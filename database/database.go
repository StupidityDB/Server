package database

import (
	"context"
	"crypto/sha256"
	"database/sql"
	"encoding/hex"
	"log"
	"runtime"

	"github.com/disgoorg/snowflake/v2"
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
		log.Fatal(err)
	}
}

func hash(s string) string {
	checksum := sha256.Sum256([]byte(s))
	return hex.EncodeToString(checksum[:])
}

func GetDiscordIDWithAuthToken(authToken string) (*snowflake.ID, error) {
	var user *User

	if err := DB.NewSelect().
		Column("DiscordID").
		Where("AuthTokenHash = ?", hash(authToken)).
		Model(user).
		Scan(context.Background()); err != nil {
		return nil, err
	}

	return &user.DiscordID, nil
}
