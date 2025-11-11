job "autocloud-app" {
  datacenters = ["dc1"]
  type        = "service"

  group "web" {
    count = 3

    network {
      port "http" {
        to = 8080
      }
    }

    service {
      name = "autocloud-web"
      port = "http"

      check {
        type     = "http"
        path     = "/health"
        interval = "10s"
        timeout  = "2s"
      }

      tags = [
        "traefik.enable=true",
        "traefik.http.routers.autocloud.rule=Host(`app.autocloud.com`)",
      ]
    }

    task "service-a" {
      driver = "docker"

      config {
        image = "autocloud/service-a:latest"
        ports = ["http"]
      }

      env {
        DB_HOST    = "${NOMAD_IP_http}"
        REDIS_HOST = "redis.service.consul"
        PORT       = "${NOMAD_PORT_http}"
      }

      resources {
        cpu    = 500
        memory = 512
      }

      scaling {
        min     = 2
        max     = 10
        enabled = true

        policy {
          cooldown            = "30s"
          evaluation_interval = "10s"

          check "cpu" {
            source = "nomad-apm"
            query  = "avg_cpu"

            strategy "target-value" {
              target = 70
            }
          }
        }
      }
    }
  }

  group "database" {
    count = 1

    network {
      port "db" {
        static = 5432
      }
    }

    task "postgres" {
      driver = "docker"

      config {
        image = "postgres:15-alpine"
        ports = ["db"]

        volumes = [
          "local/data:/var/lib/postgresql/data"
        ]
      }

      env {
        POSTGRES_USER     = "admin"
        POSTGRES_PASSWORD = "changeme"
        POSTGRES_DB       = "appdb"
      }

      resources {
        cpu    = 1000
        memory = 1024
      }
    }
  }
}
