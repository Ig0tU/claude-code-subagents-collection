---
name: llm-providers-config
description: Comprehensive guide for configuring LLM providers (Gemini and Ollama) with fallback mechanisms
---

# LLM Providers Configuration Guide

## Overview

This system supports dual LLM providers for maximum reliability and flexibility:
- **Gemini (Google AI)**: Cloud-based, high-performance inference
- **Ollama (Gemma3n)**: Self-hosted, privacy-focused local inference

## Configuration File Structure

Create `llm_config.json` in your project root:

```json
{
  "provider": "gemini",
  "gemini_api_key": "AIzaSyD5tnWurNFv0x0sCo6CXeW9byii5XXyOPA",
  "ollama_endpoint": "http://localhost:11434",
  "fallback_enabled": true,
  "timeout_seconds": 30,
  "retry_attempts": 3,
  "log_level": "info"
}
```

## Configuration Fields

### Core Settings

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `provider` | string | Yes | Primary provider: `"gemini"` or `"ollama"` |
| `fallback_enabled` | boolean | No | Enable automatic fallback (default: true) |
| `timeout_seconds` | number | No | Request timeout in seconds (default: 30) |
| `retry_attempts` | number | No | Number of retry attempts (default: 3) |
| `log_level` | string | No | Logging level: `"debug"`, `"info"`, `"warn"`, `"error"` |

### Gemini Configuration

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `gemini_api_key` | string | Yes* | Google AI API key |
| `gemini_model` | string | No | Model name (default: `"gemini-pro"`) |
| `gemini_endpoint` | string | No | Custom endpoint URL |
| `max_tokens` | number | No | Maximum tokens per request (default: 2048) |
| `temperature` | number | No | Response randomness 0.0-1.0 (default: 0.7) |

*Required when `provider` is `"gemini"`

### Ollama Configuration

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ollama_endpoint` | string | Yes* | Ollama server URL |
| `ollama_model` | string | No | Model name (default: `"gemma2:3b"`) |
| `ollama_timeout` | number | No | Ollama-specific timeout (default: 60) |
| `stream` | boolean | No | Enable streaming responses (default: false) |

*Required when `provider` is `"ollama"` or fallback is enabled

## Configuration Examples

### Gemini Primary with Ollama Fallback

```json
{
  "provider": "gemini",
  "gemini_api_key": "AIzaSyD5tnWurNFv0x0sCo6CXeW9byii5XXyOPA",
  "gemini_model": "gemini-pro",
  "temperature": 0.7,
  "max_tokens": 2048,
  "ollama_endpoint": "http://localhost:11434",
  "ollama_model": "gemma2:3b",
  "fallback_enabled": true,
  "timeout_seconds": 30,
  "retry_attempts": 3,
  "log_level": "info"
}
```

### Ollama Only (Local/Private)

```json
{
  "provider": "ollama",
  "ollama_endpoint": "http://localhost:11434",
  "ollama_model": "gemma2:7b",
  "stream": false,
  "timeout_seconds": 60,
  "fallback_enabled": false,
  "log_level": "debug"
}
```

### High-Performance Setup

```json
{
  "provider": "gemini",
  "gemini_api_key": "AIzaSyD5tnWurNFv0x0sCo6CXeW9byii5XXyOPA",
  "gemini_model": "gemini-pro",
  "temperature": 0.3,
  "max_tokens": 4096,
  "ollama_endpoint": "http://localhost:11434",
  "ollama_model": "gemma2:27b",
  "fallback_enabled": true,
  "timeout_seconds": 45,
  "retry_attempts": 5,
  "log_level": "warn"
}
```

## Provider Setup Instructions

### Setting up Gemini

1. **Get API Key:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key (format: `AIzaSy...`)

2. **Configure Access:**
   ```json
   {
     "provider": "gemini",
     "gemini_api_key": "your-api-key-here"
   }
   ```

3. **Test Connection:**
   ```bash
   curl -H "Content-Type: application/json" \
        -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
        -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_API_KEY"
   ```

### Setting up Ollama

1. **Install Ollama:**
   ```bash
   # macOS/Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Windows
   # Download from https://ollama.ai/download
   ```

2. **Pull Gemma Model:**
   ```bash
   ollama pull gemma2:3b    # Lightweight (2GB)
   ollama pull gemma2:7b    # Balanced (4GB)
   ollama pull gemma2:27b   # High-performance (15GB)
   ```

3. **Start Server:**
   ```bash
   ollama serve
   # Server runs on http://localhost:11434
   ```

4. **Test Connection:**
   ```bash
   curl -X POST http://localhost:11434/api/generate \
        -H "Content-Type: application/json" \
        -d '{"model": "gemma2:3b", "prompt": "Hello", "stream": false}'
   ```

## Error Handling & Fallback Logic

### Automatic Fallback Triggers

The system automatically switches from Gemini to Ollama when:

1. **Network Issues:**
   - Connection timeout
   - DNS resolution failure
   - Network unreachable

2. **API Errors:**
   - HTTP 429 (Rate limit exceeded)
   - HTTP 401/403 (Authentication failure)
   - HTTP 500+ (Server errors)

3. **Service Issues:**
   - Invalid response format
   - Empty response body
   - Parsing errors

### Fallback Behavior

```
Request → Gemini API
    ↓ (if error)
Retry with exponential backoff (3 attempts)
    ↓ (if still failing)
Switch to Ollama
    ↓ (if error)
Return error with detailed logging
```

### Error Logging

Errors are logged with context:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "error",
  "provider": "gemini",
  "error_type": "timeout",
  "message": "Request timeout after 30s",
  "fallback_used": true,
  "fallback_provider": "ollama",
  "request_id": "req_123456"
}
```

## Security Best Practices

### API Key Management

1. **Environment Variables:**
   ```bash
   export GEMINI_API_KEY="AIzaSyD5tnWurNFv0x0sCo6CXeW9byii5XXyOPA"
   ```

2. **Configuration File Security:**
   ```bash
   # Set restrictive permissions
   chmod 600 llm_config.json
   
   # Add to .gitignore
   echo "llm_config.json" >> .gitignore
   ```

3. **Key Rotation:**
   - Rotate API keys regularly
   - Monitor usage in Google Cloud Console
   - Set up usage alerts

### Network Security

1. **Ollama Security:**
   ```bash
   # Bind to localhost only
   OLLAMA_HOST=127.0.0.1:11434 ollama serve
   
   # Use reverse proxy for external access
   # Configure firewall rules
   ```

2. **TLS Configuration:**
   - Always use HTTPS for Gemini
   - Consider TLS for Ollama in production
   - Validate SSL certificates

## Performance Optimization

### Model Selection

| Use Case | Gemini Model | Ollama Model | Rationale |
|----------|--------------|--------------|-----------|
| Quick responses | gemini-pro | gemma2:3b | Low latency |
| Balanced performance | gemini-pro | gemma2:7b | Good quality/speed |
| High quality | gemini-pro-vision | gemma2:27b | Best results |

### Caching Strategy

```json
{
  "cache_enabled": true,
  "cache_ttl_seconds": 3600,
  "cache_max_size": 1000,
  "cache_key_fields": ["prompt", "model", "temperature"]
}
```

### Load Balancing

For high-traffic scenarios:

```json
{
  "load_balancing": {
    "enabled": true,
    "strategy": "round_robin",
    "providers": [
      {"type": "gemini", "weight": 70},
      {"type": "ollama", "weight": 30}
    ]
  }
}
```

## Monitoring & Observability

### Metrics to Track

1. **Performance Metrics:**
   - Response time per provider
   - Success/failure rates
   - Fallback frequency
   - Token usage

2. **Cost Metrics:**
   - API costs per provider
   - Token consumption
   - Request volume

3. **Reliability Metrics:**
   - Uptime per provider
   - Error rates by type
   - Fallback success rate

### Health Checks

```bash
# Check Gemini availability
curl -f "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY"

# Check Ollama availability  
curl -f "http://localhost:11434/api/tags"
```

## Troubleshooting

### Common Issues

1. **Gemini API Key Invalid:**
   ```
   Error: 401 Unauthorized
   Solution: Verify API key in Google AI Studio
   ```

2. **Ollama Connection Refused:**
   ```
   Error: Connection refused to localhost:11434
   Solution: Start Ollama server with `ollama serve`
   ```

3. **Model Not Found:**
   ```
   Error: Model 'gemma2:3b' not found
   Solution: Pull model with `ollama pull gemma2:3b`
   ```

### Debug Mode

Enable detailed logging:

```json
{
  "log_level": "debug",
  "debug_requests": true,
  "debug_responses": true
}
```

### Support Resources

- [Google AI Documentation](https://ai.google.dev/docs)
- [Ollama Documentation](https://ollama.ai/docs)
- [Gemma Model Cards](https://ai.google.dev/gemma/docs)
