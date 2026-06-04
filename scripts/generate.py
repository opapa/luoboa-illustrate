#!/usr/bin/env python
"""Generate images for WeChat articles using GPT-image-2 compatible APIs.

Usage:
  python generate.py cover --prompt "..." --output path/to/cover.png [--style tech]
  python generate.py section --prompt "..." --output path/to/section.png [--ref-url URL]

Config:
  Reads config.yaml from the skill root directory for API and brand settings.
  If config.yaml is missing, falls back to environment variables:
    GPT_IMAGE_API_KEY  - API key
    GPT_IMAGE_API_URL  - API base URL (default: https://api.openai.com)
"""

import json, urllib.request, ssl, sys, os


# --- Minimal YAML parser (no external dependency) ---

def parse_yaml(text):
    """Parse a simple subset of YAML into a dict.

    Supports: key: value, nested sections via indentation, # comments,
    quoted strings, null, true/false. No lists, anchors, or multiline values.
    """
    result = {}
    # Stack of (indent_level, dict_object)
    stack = [(0, result)]

    for line in text.splitlines():
        stripped = line.rstrip()
        if not stripped or stripped.lstrip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())
        content = stripped.strip()

        # Pop stack until we find the parent at a lower indent
        while len(stack) > 1 and stack[-1][0] >= indent:
            stack.pop()

        if ":" not in content:
            continue

        key, _, value = content.partition(":")
        key = key.strip()
        value = value.strip()

        if not value:
            # New section
            new_dict = {}
            stack[-1][1][key] = new_dict
            stack.append((indent, new_dict))
        else:
            # Key-value pair
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            elif value.lower() == "null":
                value = None
            elif value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            else:
                # Try number
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        pass  # keep as string

            stack[-1][1][key] = value

    return result


# --- Config loading ---

def load_config():
    """Load config.yaml from the skill root directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_root = os.path.dirname(script_dir)
    config_path = os.path.join(skill_root, "config.yaml")

    if not os.path.exists(config_path):
        return {}

    with open(config_path, "r", encoding="utf-8") as f:
        return parse_yaml(f.read())


CONFIG = load_config()

# --- API settings ---

api_config = CONFIG.get("api", {})
API_KEY = api_config.get("api_key", os.environ.get("GPT_IMAGE_API_KEY", ""))
API_BASE = api_config.get("base_url", os.environ.get("GPT_IMAGE_API_URL", "https://api.openai.com"))
API_MODEL = api_config.get("model", "gpt-image-2")
PROVIDER = api_config.get("provider", "openai")

# Provider-specific endpoint defaults
if PROVIDER == "grsai":
    COVER_ENDPOINT = "/v1/images/generations"
    SECTION_ENDPOINT = "/v1/draw/completions"
    USE_SSE_SECTION = True
else:
    # openai, openai-compatible, local
    COVER_ENDPOINT = "/v1/images/generations"
    SECTION_ENDPOINT = "/v1/images/generations"
    USE_SSE_SECTION = False

# --- Brand settings (multi-profile) ---

brand_config = CONFIG.get("brand", {})
BRAND_ENABLED = brand_config.get("enabled", False)
BRAND_DEFAULT = brand_config.get("default", "luoboa")
BRAND_PROFILES = brand_config.get("profiles", {})
BRAND_TYPE_ROUTING = brand_config.get("type_routing", {})

# Styles that support brand watermark
# (Extended to cover all "professional outward-facing" content types)
BRANDED_STYLES = {
    # 科技向
    "tech", "blueprint", "cyberpunk-neon", "corporate", "pixel-art",
    "sketch-notes", "vintage", "watercolor", "screen-print", "zen-minimal",
    # 工具/生活向
    "food", "travel", "home", "fashion", "pet", "kawaii",
    "infographic", "sports", "digital-illustration", "painterly",
}


def resolve_brand(article_type=None, brand_override=None):
    """Resolve the active brand profile.

    Priority: brand_override (CLI) > type_routing[article_type] > default

    Returns: dict with keys {name, tagline, logo_url, handle, key}
    Returns None if brand is disabled or no profile found.
    """
    if not BRAND_ENABLED:
        return None

    key = brand_override
    if not key and article_type:
        key = BRAND_TYPE_ROUTING.get(article_type)
    if not key:
        key = BRAND_DEFAULT
    if not key or key not in BRAND_PROFILES:
        return None

    profile = BRAND_PROFILES[key]
    return {
        "key": key,
        "name": profile.get("name", ""),
        "tagline": profile.get("tagline", ""),
        "logo_url": profile.get("logo_url"),
        "website": profile.get("handle", ""),
    }


def build_watermark_prompt(brand):
    """Build the watermark text snippet for the prompt.

    Text-only mode (no logo image): brand name + tagline + website
    With logo image: same text PLUS the logo will be composited by the API
    """
    if not brand:
        return ""
    parts = [f"Brand watermark at bottom-right corner: '{brand['name']}'"]
    if brand.get("tagline"):
        parts.append(f"tagline '{brand['tagline']}'")
    if brand.get("handle"):
        parts.append(f"website '{brand['website']}'")
    if brand.get("logo_url"):
        parts.append("plus a brand logo image (composited via API)")
    return " · ".join(parts) + "."


# Backward-compat constants (used by generate_cover/section if no brand resolution done)
# When article_type is unknown, fall back to legacy single-brand behavior
_LEGACY_BRAND = {
    "name": brand_config.get("name", ""),
    "tagline": brand_config.get("tagline", ""),
    "logo_url": brand_config.get("logo_url"),
    "website": brand_config.get("handle", ""),
}


def should_include_brand(style=None, article_type=None, brand_override=None):
    """Check if brand should be included based on config and style.

    New: passes article_type and brand_override through to resolve_brand().
    """
    brand = resolve_brand(article_type, brand_override)
    if not brand:
        return False, None
    if style and style.lower() not in BRANDED_STYLES:
        return False, None
    return True, brand


# --- Image generation ---

def _make_request(endpoint, payload):
    """Make an API request and return the parsed JSON response."""
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        f"{API_BASE}{endpoint}",
        data=data,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=180, context=ctx) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code} {e.reason}: {body[:1500]}", file=sys.stderr)
        raise


def _make_sse_request(payload):
    """Make an SSE API request (for grsai section illustrations)."""
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        f"{API_BASE}{SECTION_ENDPOINT}",
        data=data,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
    )
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=180, context=ctx) as resp:
        result = resp.read().decode("utf-8")
        for line in result.strip().split("\n"):
            if line.startswith("data: "):
                obj = json.loads(line[6:])
                if obj.get("status") == "succeeded":
                    return obj["results"][0]["url"]
                elif obj.get("status") == "failed":
                    raise RuntimeError(f"API failed: {obj.get('failure_reason', 'unknown')}")
    raise RuntimeError("SSE stream ended without result")


def generate_cover(prompt, output_path, style=None, article_type=None, brand_override=None):
    """Generate a cover image (1920x832).

    article_type: one of tech/career/growth/profile/opinion/zhihu/healing/toutiao/yeting/riting/fiction
                  — used to auto-route brand via type_routing
    brand_override: explicit brand key to use (overrides article_type routing)

    If prompt already includes brand watermark text, this function also
    passes logo_url to the API when set (for image compositing).
    """
    include, brand = should_include_brand(style, article_type, brand_override)
    payload = {
        "model": API_MODEL,
        "prompt": prompt,
        "size": "1920x832",
        "response_format": "url"
    }

    if include and brand and brand.get("logo_url"):
        # Has logo image → API will composite it onto the cover
        payload["image"] = [brand["logo_url"]]
    elif include and brand:
        # Text-only brand (no logo URL) → already in the prompt
        pass

    result = _make_request(COVER_ENDPOINT, payload)
    urllib.request.urlretrieve(result["data"][0]["url"], output_path)
    print(f"OK: {output_path}")
    if brand:
        print(f"Brand: {brand['key']} ({brand['name']})")


def generate_section(prompt, output_path, ref_url=None, style=None, aspect_ratio=None, article_type=None, brand_override=None):
    """Generate a section illustration.

    aspect_ratio: e.g. "1024x1024" (default 1:1), "1024x1792" (9:16), "1792x1024" (16:9), etc.
    article_type / brand_override: same as generate_cover
    """
    if aspect_ratio is None:
        aspect_ratio = "1024x1024"
    returned_url = None

    include, brand = should_include_brand(style, article_type, brand_override)

    if USE_SSE_SECTION:
        # grsai provider: SSE endpoint with aspectRatio
        payload = {
            "model": API_MODEL,
            "prompt": prompt,
            "aspectRatio": aspect_ratio,
            "replyType": "async"
        }
        if ref_url:
            payload["image"] = [ref_url]
        elif include and brand and brand.get("logo_url"):
            payload["image"] = [brand["logo_url"]]

        try:
            returned_url = _make_sse_request(payload)
        except RuntimeError as e:
            if ref_url and "failed" in str(e).lower():
                print("Retrying without reference image...")
                payload.pop("image", None)
                returned_url = _make_sse_request(payload)
            else:
                raise
    else:
        # openai / openai-compatible / local: standard endpoint
        payload = {
            "model": API_MODEL,
            "prompt": prompt,
            "size": aspect_ratio,
            "response_format": "url"
        }
        if ref_url:
            payload["image"] = [ref_url]
        elif include and brand and brand.get("logo_url"):
            payload["image"] = [brand["logo_url"]]

        result = _make_request(SECTION_ENDPOINT, payload)
        returned_url = result["data"][0]["url"]

    urllib.request.urlretrieve(returned_url, output_path)
    print(f"OK: {output_path}")
    print(f"REF_URL: {returned_url}")
    return returned_url


# --- CLI ---

def main():
    if not API_KEY:
        print("ERROR: API key not configured. Run the setup wizard or set GPT_IMAGE_API_KEY env var.")
        sys.exit(1)

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    mode = sys.argv[1]

    # Parse --key value arguments
    args = {}
    i = 2
    while i < len(sys.argv):
        if sys.argv[i].startswith("--"):
            key = sys.argv[i][2:]
            if i + 1 < len(sys.argv) and not sys.argv[i+1].startswith("--"):
                args[key] = sys.argv[i+1]
                i += 2
            else:
                args[key] = True
                i += 1
        else:
            i += 1

    prompt = args.get("prompt", "")
    output = args.get("output", "")
    ref_url = args.get("ref-url", None)
    style = args.get("style", None)
    aspect_ratio = args.get("aspect-ratio", None)
    article_type = args.get("article-type", None)
    brand_override = args.get("brand", None)

    if not prompt or not output:
        print("ERROR: --prompt and --output are required")
        sys.exit(1)

    if mode == "cover":
        generate_cover(prompt, output, style, article_type, brand_override)
    elif mode == "section":
        generate_section(prompt, output, ref_url, style, aspect_ratio, article_type, brand_override)
    else:
        print(f"ERROR: Unknown mode '{mode}'. Use 'cover' or 'section'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
