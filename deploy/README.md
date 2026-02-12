# Deploy

## PostgreSQL (local / dev)

From this directory:

```bash
docker compose up -d
```

Connect from your machine:

| Setting   | Value                |
|----------|----------------------|
| Host     | `localhost`           |
| Port     | `5432`                |
| User     | `postgres`            |
| Password | `postgres`            |
| Database | `neighborhood_library` |

**Connection string:**  
`postgresql://postgres:postgres@localhost:5432/neighborhood_library`

Stop:

```bash
docker compose down
```

Data is stored in the `postgres_data` volume.
