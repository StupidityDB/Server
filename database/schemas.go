package database

import (
	"context"
	"time"

	"github.com/disgoorg/snowflake/v2"
	"github.com/uptrace/bun"
)

type UserType int8

const (
	UserBanned = iota - 1
	UserNormal
	UserAdmin
)

type CModFlags uint8

const (
	CModAliucord CModFlags = 1 << iota
	CModBetterDiscord
	CModPowercordV2
	CModReplugged
	CModEnmity
	CModVencord
	CModVendetta
)

type BadgeFlags uint8

const (
	BadgeDeveloper BadgeFlags = 1 << iota
	BadgeDonator
	BadgeINSANE
	BadgeUwU
)

type User struct {
	bun.BaseModel `bun:"table:Users"`

	DiscordID       snowflake.ID `bun:"DiscordID, pk"`
	Username        string       `bun:"Username"`
	ProfilePhotoURL string       `bun:"ProfilePhotoURL"`

	Type       UserType   `bun:"Type"`
	ClientMods CModFlags  `bun:"ClientModFlags"`
	Badges     BadgeFlags `bun:"BadgeFlags"`

	AuthToken string `bun:"AuthToken"`
}

/* StupidityDB */

type StupidityVote struct {
	bun.BaseModel `bun:"table:StupidityVotes"`

	RaterDiscordID snowflake.ID `bun:"RaterDiscordID"`
	// Minimum 0, maximum 100.
	Rating uint8 `bun:"Rating"`

	RatedDiscordID snowflake.ID `bun:"RatedDiscordID"`
}

/* ReviewDB */

type ReviewType uint8

const (
	ReviewToUser ReviewType = iota
	ReviewToServer
	ReviewPlsDonate
	ReviewSystem
)

type Review struct {
	bun.BaseModel `bun:"table:Reviews"`

	ID        uint32     `bun:"ID, pk, autoincrement"`
	Type      ReviewType `bun:"Type"`
	Stars     uint32     `bun:"Stars"`
	Content   string     `bun:"Content"`
	Timestamp time.Time  `bun:"Timestamp, default:current_timestamp"`

	ReviewerDiscordID snowflake.ID `bun:"ReviewerDiscordID"`
	ReviewedDiscordID snowflake.ID `bun:"ReviewedDiscordID"`
}

func createSchemas() error {
	models := []any{
		(*User)(nil),
		(*StupidityVote)(nil),
		(*Review)(nil),
	}

	for _, model := range models {
		if _, err := DB.NewCreateTable().IfNotExists().Model(model).Exec(context.Background()); err != nil {
			return err
		}
	}

	return nil
}
