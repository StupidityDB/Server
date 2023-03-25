package database

import (
	"database/sql"
	"log"
	"runtime"

	"github.com/uptrace/bun"
	"github.com/uptrace/bun/dialect/pgdialect"
	"github.com/uptrace/bun/driver/pgdriver"

	"server-go/config"
)

var DB *bun.DB

func init() {
	Config := config.Config.DB

	DB = bun.NewDB(
		sql.OpenDB(
			pgdriver.NewConnector(
				pgdriver.WithAddr(Config.IP),
				pgdriver.WithUser(Config.User),
				pgdriver.WithDatabase(Config.Name),
				pgdriver.WithPassword(Config.Password),
				pgdriver.WithTLSConfig(nil),
			),
		), pgdialect.New(),
	)

	maxOpenConns := 4 * runtime.GOMAXPROCS(0)
	DB.SetMaxOpenConns(maxOpenConns)
	DB.SetMaxIdleConns(maxOpenConns)

	if err := createSchemas(); err != nil {
		log.Fatalf("Failed to create schemas: %v", err)
	}
}
