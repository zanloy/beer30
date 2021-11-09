# beer30

This is the beer30 bot/site.

## Configuration

These are the configuration items for beer30:

| Name         | ENV Variable         | Parameter                                     | Type      | Default           |
| ------------ | -------------------- | --------------------------------------------- | --------- | ----------------- |
| HTTP port    | `BEER30_PORT`        | `--port`                                      | integer   | `8080`            |
| Slack Token  | `BEER30_SLACK_TOKEN` | `--token`                                     | string    |`None` (required)  |
| Password     | `BEER30_PASSWORD`    | `--password PASSWORD`                         | string    | Random string     |
| Log Level    | `BEER30_LOG_LEVEL`   | [`CRITICAL`,`ERROR`,`WARNING`,`INFO`,`DEBUG`] | string    | `WARNING`         |
| Slack admins | None                 | `--admins ADMIN1 ADMIN2`                      | string    | `None` (required) |