# Shopify GraphQL Image Upload (2026-07-07)

## Problem
Shopify Admin REST API 2024-10 returns `HTTP 406` for:
- `POST /staged_uploads.json` with JSON payload
- `POST /product_images.json` with JSON `attachment`/`src`
- `POST /product_images.json` with multipart form-data

## Solution: Three-Step GraphQL Flow

### Step 1: Create Staged Upload Target
```graphql
mutation stagedUploadCreate($input: [StagedUploadInput!]!) {
  stagedUploadsCreate(input: $input) {
    stagedTargets {
      url
      resourceUrl
      parameters { name value }
    }
    userErrors { field message }
  }
}
```

Variables:
```json
{
  "input": [{
    "filename": "lifestyle_oat_desk_mat.jpg",
    "resource": "IMAGE",
    "mimeType": "image/jpeg",
    "httpMethod": "POST",
    "fileSize": "199507"
  }]
}
```

**Critical**: `fileSize` must be a **string**, not int. Shopify returns:
```
UnsignedInt64 '199507' must be encoded as a string
```

Returns:
- `url`: POST target for binary upload
- `resourceUrl`: final Shopify asset URL after upload
- `parameters`: auth headers (key, x-goog-date, x-goog-credential, x-goog-signature, etc.)

### Step 2: Upload Binary to Staged URL
```python
files = {'file': (fname, file_data, 'image/jpeg')}
params = {p['name']: p['value'] for p in target['parameters']}
r = requests.post(upload_url, files=files, data=params, timeout=60)
# Expect HTTP 201
```

### Step 3: Create Product Media
```graphql
mutation productCreateMedia($productId: ID!, $media: [CreateMediaInput!]!) {
  productCreateMedia(productId: $productId, media: $media) {
    media { id preview { status image { url } } }
    product { id }
    userErrors { field message }
  }
}
```

Variables:
```json
{
  "productId": "gid://shopify/Product/8912640311375",
  "media": [{
    "originalSource": "https://shopify-staged-uploads.storage.googleapis.com/tmp/...",
    "mediaContentType": "IMAGE"
  }]
}
```

**Field name rules**:
- `altText` does NOT exist on `Media` type → causes GraphQL error
- Use only `originalSource` + `mediaContentType` for `CreateMediaInput`
- `status` in mutation must be uppercase: `ACTIVE`, `ARCHIVED`, `DRAFT`

## Verified Working
- Shop: dbd9ub-8a.myshopify.com
- API version: 2024-10
- Theme ID: 147575734351
- Tested on 2026-07-07 with 21 lifestyle mockup JPGs (~200KB each)
- All 21 uploads succeeded with `preview.status = UPLOADED`

## Do Not Retry
- REST `POST /product_images.json` with JSON body
- REST `POST /staged_uploads.json` with JSON body
- REST multipart `image[attachment]` or `image[src]`
