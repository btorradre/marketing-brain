# Workflow JSON Templates & Examples

## Minimal Two-Node Workflow — Webhook → Slack

This is the actual shape a workflow's JSON takes: a `nodes` array (each node fully specified — id, name, type, typeVersion, position, parameters) plus a `connections` object wiring them together.
```javascript
{
  "name": "Webhook to Slack",
  "nodes": [
    {
      "id": "webhook-1",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [250, 300],
      "parameters": {
        "path": "slack-notify",
        "httpMethod": "POST"
      }
    },
    {
      "id": "slack-1",
      "name": "Slack",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2,
      "position": [450, 300],
      "parameters": {
        "resource": "message",
        "operation": "post",
        "channel": "#general",
        "text": "={{$json.body.message}}"
      }
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{ "node": "Slack", "type": "main", "index": 0 }]]
    }
  }
}
```
Note the webhook payload is accessed as `$json.body.message` — n8n's Webhook node nests all incoming POST data, query params, and headers under a `body`/`query`/`headers` structure.

## IF Node Branch Wiring
```javascript
"connections": {
  "IF": {
    "main": [
      [{ "node": "True Handler", "type": "main", "index": 0 }],   // output 0 = condition true
      [{ "node": "False Handler", "type": "main", "index": 0 }]   // output 1 = condition false
    ]
  }
}
```

## Switch Node Branch Wiring (3 cases)
```javascript
"connections": {
  "Switch": {
    "main": [
      [{ "node": "Handler A", "type": "main", "index": 0 }],  // case 0
      [{ "node": "Handler B", "type": "main", "index": 0 }],  // case 1
      [{ "node": "Handler C", "type": "main", "index": 0 }]   // case 2
    ]
  }
}
```

## Credential Reference on a Node
```javascript
{
  "id": "http-1",
  "name": "Call Internal API",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4,
  "position": [450, 300],
  "parameters": {
    "method": "POST",
    "url": "https://api.example.com/users"
  },
  "credentials": {
    "httpHeaderAuth": {
      "id": "abc123",
      "name": "My API Key"
    }
  }
}
```

## AI Agent with a Language Model and a Tool Wired In
```javascript
{
  "nodes": [
    { "id": "1", "name": "OpenAI Chat Model", "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi", "typeVersion": 1, "position": [200, 200], "parameters": {} },
    { "id": "2", "name": "HTTP Request Tool", "type": "@n8n/n8n-nodes-langchain.toolHttpRequest", "typeVersion": 1, "position": [200, 400], "parameters": {} },
    { "id": "3", "name": "AI Agent", "type": "@n8n/n8n-nodes-langchain.agent", "typeVersion": 1, "position": [450, 300], "parameters": {} }
  ],
  "connections": {
    "OpenAI Chat Model": { "ai_languageModel": [[{ "node": "AI Agent", "type": "ai_languageModel", "index": 0 }]] },
    "HTTP Request Tool": { "ai_tool": [[{ "node": "AI Agent", "type": "ai_tool", "index": 0 }]] }
  }
}
```

## Binary vs Unary Condition Example (Filter/IF Node)
```javascript
// Binary — comparing title text to a keyword
{
  "conditions": [
    {
      "leftValue": "={{$json.title}}",
      "rightValue": "urgent",
      "operator": { "type": "string", "operation": "contains" }   // no singleValue
    }
  ]
}

// Unary — checking a field is present
{
  "conditions": [
    {
      "leftValue": "={{$json.email}}",
      "operator": { "type": "string", "operation": "isNotEmpty", "singleValue": true }
    }
  ]
}
```

## Data Table Row Filter Shape
```javascript
// Filter: rows where status = "active"
{
  "filters": [
    { "columnName": "status", "condition": "eq", "value": "active" }
  ]
}

// Filter: rows where score < 5 (for a bulk update — always preview with a filter like this before mutating)
{
  "filters": [
    { "columnName": "score", "condition": "lt", "value": 5 }
  ]
}
```

## Security-Scan Patterns Worth Running Over Exported Workflow JSON
```javascript
// Loose starting points — tighten per platform as needed
const patterns = {
  openaiKey: /sk-[A-Za-z0-9]{20,}/,
  slackToken: /xox[baprs]-[A-Za-z0-9-]{10,}/,
  awsKey: /AKIA[0-9A-Z]{16}/,
  email: /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/,
  genericSecretField: /"(api[_-]?key|secret|password|token)"\s*:\s*"[^"]{8,}"/i
};
```
Run these against a node's `parameters` block specifically (not its `credentials` block, which should never contain the raw secret in the first place) — a hit there is very likely a hardcoded secret that should be moved into a proper stored credential.
