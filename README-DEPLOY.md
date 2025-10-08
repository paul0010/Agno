# Deploying Agno Agent to Dokploy

This guide explains how to deploy your Agno agent as a production API using Dokploy.

## Prerequisites

- Dokploy instance (self-hosted or cloud)
- Git repository (GitHub, GitLab, Gitea, or Bitbucket)
- API keys:
  - Google Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))
  - Tavily API key ([Get it here](https://tavily.com))

## Project Structure

```
.
├── agno_agent.py          # Main agent application
├── Dockerfile             # Docker configuration
├── requirements.txt       # Python dependencies
├── .dockerignore         # Docker build exclusions
├── .env.example          # Environment variables template
└── README-DEPLOY.md      # This file
```

## Deployment Steps

### 1. Prepare Your Repository

1. Push your code to a Git repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Agno agent for Dokploy"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

### 2. Configure Dokploy Application

1. **Login to Dokploy Dashboard**
   - Access your Dokploy instance

2. **Create New Application**
   - Click "Create Application"
   - Choose "Application" type

3. **Connect Repository**
   - Select your Git provider (GitHub/GitLab/etc.)
   - Choose the repository containing your Agno agent
   - Select the `main` branch (or your deployment branch)

4. **Configure Build Settings**
   - **Build Type**: Dockerfile
   - **Dockerfile Path**: `./Dockerfile`
   - **Context Path**: `.` (root directory)

### 3. Set Environment Variables

In Dokploy's Environment Variables section, add:

```env
GOOGLE_API_KEY=your_actual_google_api_key
TAVILY_API_KEY=your_actual_tavily_api_key
DB_DIR=/code/data
```

**Important**: Never commit actual API keys to your repository!

### 4. Configure Volumes (Persistent Storage)

To persist your SQLite database across deployments:

1. Go to **Volumes** section in Dokploy
2. Add new volume:
   - **Host Path**: `/var/lib/dokploy/agno-data` (or your preferred path)
   - **Container Path**: `/code/data`
   - **Type**: Bind mount

### 5. Configure Port & Domain

1. **Port Configuration**
   - **Container Port**: 8000
   - **Public Port**: 80 or 443 (handled by Traefik)

2. **Domain Setup**
   - Use Dokploy-generated domain (e.g., `app.traefik.me`)
   - Or configure custom domain

### 6. Deploy

1. Click **Deploy** button
2. Monitor build logs
3. Wait for deployment to complete

## API Endpoints

Once deployed, your API will be available at:

- **API Documentation**: `https://your-domain/docs`
- **Agent Chat Endpoint**: `https://your-domain/v1/agents/Agno Agent/sessions/{session_id}/chat`
- **Health Check**: `https://your-domain/health` (if configured)

### Example API Usage

```bash
# Create a new session and chat
curl -X POST "https://your-domain/v1/agents/Agno%20Agent/sessions/my-session/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the latest trends in AI?",
    "stream": false
  }'
```

## Local Testing (Before Deployment)

Test your Docker container locally:

```bash
# Build the image
docker build -t agno-agent .

# Run the container
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY=your_key \
  -e TAVILY_API_KEY=your_key \
  -v $(pwd)/data:/code/data \
  agno-agent

# Access API docs at http://localhost:8000/docs
```

## Troubleshooting

### Common Issues

1. **Database Errors**
   - Ensure volume is properly mounted
   - Check `/code/data` directory permissions

2. **API Key Errors**
   - Verify environment variables are set in Dokploy
   - Check variable names match exactly

3. **Build Failures**
   - Review Dokploy build logs
   - Ensure all dependencies are in `requirements.txt`

4. **Connection Timeout**
   - Verify port 8000 is exposed
   - Check Traefik routing configuration

### View Logs

In Dokploy dashboard:
- Go to your application
- Click **Logs** tab
- Monitor real-time application logs

## Auto-Deployment

Enable automatic deployments on git push:

1. Go to **Settings** in Dokploy
2. Enable **Auto Deploy**
3. Configure webhook in your Git repository
4. Every push to main branch will trigger deployment

## Scaling (Optional)

For production workloads, modify `Dockerfile` to adjust workers:

```dockerfile
# Change workers count based on your needs
CMD ["uvicorn", "agno_agent:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "8"]
```

## Security Best Practices

1. **Never commit `.env` file** - Use Dokploy's environment variables
2. **Use HTTPS** - Configure SSL/TLS in Dokploy
3. **Implement authentication** - Add JWT or API key middleware (see Agno docs)
4. **Rate limiting** - Configure in Dokploy or add to FastAPI app
5. **Regular updates** - Keep dependencies updated

## Resources

- [Agno Documentation](https://docs.agno.com)
- [Dokploy Documentation](https://docs.dokploy.com)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## Support

For issues:
- Agno: [GitHub Issues](https://github.com/agno-agi/agno/issues)
- Dokploy: [GitHub Issues](https://github.com/Dokploy/dokploy/issues)
