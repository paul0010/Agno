# AgentOS UI Setup Guide

Your Agno agent API is running, now let's add a beautiful UI to interact with it!

## Option 1: Use the Official Agno Agent UI (Recommended)

The official Agent UI is a modern Next.js chat interface built specifically for AgentOS.

### Quick Start with NPX

```bash
npx create-agent-ui@latest
cd agent-ui
npm run dev
```

The UI will start on `http://localhost:3000` and connect to your AgentOS API.

### Configure Connection to Your Dokploy API

Edit the Agent UI configuration to point to your deployed API:

1. In the Agent UI project, create/edit `.env.local`:
```env
NEXT_PUBLIC_AGENTOS_URL=https://your-dokploy-domain.com
```

2. Start the UI:
```bash
npm run dev
```

### Deploy Agent UI to Dokploy

**Option A: Deploy as a separate application**

1. Push Agent UI to a separate GitHub repository
2. Create new application in Dokploy
3. Set build type to "Node.js" or "Dockerfile"
4. Add environment variable:
   ```
   NEXT_PUBLIC_AGENTOS_URL=https://your-api-domain.com
   ```
5. Deploy

**Option B: Use the hosted Agent UI**

Visit the official Agno playground and connect to your API endpoint.

---

## Option 2: Clone and Customize

For more control, clone the repository:

```bash
git clone https://github.com/agno-agi/agent-ui.git
cd agent-ui
pnpm install
pnpm dev
```

### Environment Configuration

Create `.env.local`:
```env
# Your AgentOS API URL
NEXT_PUBLIC_AGENTOS_URL=https://your-dokploy-domain.com

# Optional: Custom branding
NEXT_PUBLIC_APP_NAME=My AI Agent
```

---

## Option 3: Build Your Own UI

Your AgentOS API is standard REST, so you can build any UI:

### Key API Endpoints

```javascript
// Get agent info
GET https://your-domain.com/v1/agents

// Chat with agent
POST https://your-domain.com/v1/agents/{agent_name}/sessions/{session_id}/chat
Body: {
  "message": "Hello!",
  "stream": true
}

// Get session history
GET https://your-domain.com/v1/agents/{agent_name}/sessions/{session_id}
```

### Example: Simple HTML Chat Interface

```html
<!DOCTYPE html>
<html>
<head>
    <title>Agno Agent Chat</title>
</head>
<body>
    <div id="chat"></div>
    <input id="message" type="text" placeholder="Type message...">
    <button onclick="sendMessage()">Send</button>

    <script>
        const API_URL = 'https://your-dokploy-domain.com';
        const AGENT_NAME = 'Agno Agent';
        const SESSION_ID = 'user-' + Date.now();

        async function sendMessage() {
            const input = document.getElementById('message');
            const message = input.value;
            input.value = '';

            // Display user message
            document.getElementById('chat').innerHTML +=
                `<p><strong>You:</strong> ${message}</p>`;

            // Send to API
            const response = await fetch(
                `${API_URL}/v1/agents/${encodeURIComponent(AGENT_NAME)}/sessions/${SESSION_ID}/chat`,
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message, stream: false })
                }
            );

            const data = await response.json();

            // Display agent response
            document.getElementById('chat').innerHTML +=
                `<p><strong>Agent:</strong> ${data.content}</p>`;
        }
    </script>
</body>
</html>
```

---

## Features of Official Agent UI

- ✅ **Real-time streaming** - See responses as they're generated
- ✅ **Tool calls visualization** - Watch agent use tools
- ✅ **Reasoning steps** - See agent's thought process
- ✅ **Multi-modal support** - Images, video, audio
- ✅ **Session history** - Review past conversations
- ✅ **Mobile responsive** - Works on all devices
- ✅ **Dark mode** - Eye-friendly interface

---

## Deployment Architecture Options

### Architecture 1: Separate Deployments (Recommended)
```
User Browser
    ↓
Agent UI (Dokploy App #1)
    ↓
AgentOS API (Dokploy App #2) ← Your current deployment
```

**Benefits:**
- Independent scaling
- Easier updates
- Better security

### Architecture 2: Combined Deployment
```
User Browser
    ↓
Single Dokploy App
├── Next.js UI (frontend)
└── FastAPI (backend)
```

**Benefits:**
- Single deployment
- Shared environment variables
- Simplified management

---

## Quick Deploy Agent UI to Dokploy

### Step 1: Create Agent UI Repository

```bash
# Initialize Agent UI
npx create-agent-ui@latest my-agent-ui
cd my-agent-ui

# Initialize git
git init
git add .
git commit -m "Initial Agent UI setup"

# Push to GitHub
git remote add origin https://github.com/your-username/my-agent-ui.git
git push -u origin main
```

### Step 2: Deploy to Dokploy

1. **Create New Application** in Dokploy
2. **Connect Repository**: `your-username/my-agent-ui`
3. **Build Type**: Node.js / Dockerfile
4. **Environment Variables**:
   ```
   NEXT_PUBLIC_AGENTOS_URL=https://your-api-domain.com
   ```
5. **Port**: 3000
6. **Deploy**

### Step 3: Access Your UI

Visit your Agent UI domain and start chatting with your Agno agent!

---

## Troubleshooting

### UI Can't Connect to API

**Issue**: CORS errors or connection refused

**Solution**: Add CORS middleware to your AgentOS API

Edit `agno_agent.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

# After creating app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your UI domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Streaming Not Working

**Issue**: Messages don't stream in real-time

**Solution**: Ensure your Dokploy/Traefik configuration supports SSE (Server-Sent Events)

---

## Resources

- [Agno Agent UI GitHub](https://github.com/agno-agi/agent-ui)
- [AgentOS Documentation](https://docs.agno.com/agent-os)
- [AG-UI Protocol](https://docs.agno.com/agent-os/interfaces/ag-ui/introduction)
- [Next.js Deployment](https://nextjs.org/docs/deployment)

---

## Summary

You have 3 main options:

1. **Quick & Easy**: Use `npx create-agent-ui@latest` locally
2. **Production**: Deploy Agent UI as separate Dokploy app
3. **Custom**: Build your own UI using the REST API

Your AgentOS API is fully functional and ready to accept connections from any UI!
