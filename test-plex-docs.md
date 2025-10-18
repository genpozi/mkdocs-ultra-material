# Plex

## Overview



## Quick Reference

- **Status**: Active
- **Host**: homelab.local
- **Port**: 32400
- **Container**: plex
- **Image**: N/A

## Configuration

### Docker Compose

```yaml
services:
  plex:
    image: 
    container_name: plex
    
    
    
    restart: unless-stopped
```

### Environment Variables


No environment variables configured.


## Access





## Maintenance

### Backup

```bash
# Backup configuration
docker exec plex backup-command

# Backup volumes
docker run --rm -v plex_data:/data -v $(pwd):/backup alpine tar czf /backup/plex-backup-$(date +%Y%m%d).tar.gz /data
```

### Update

```bash
# Pull latest image
docker compose pull plex

# Restart service
docker compose up -d plex
```

### Logs

```bash
# View logs
docker compose logs -f plex

# Last 100 lines
docker compose logs --tail=100 plex
```

## Troubleshooting

### Common Issues


<!-- AI-GENERATE: List 3 common issues for Plex and their solutions -->


### Health Check

```bash
# Check container status
docker ps | grep plex

# Check resource usage
docker stats plex --no-stream

# Test connectivity

docker exec plex health-check-command

```

## Notes



---

**Last Updated**: {{ now }}
**Maintained By**: Homelab Admin