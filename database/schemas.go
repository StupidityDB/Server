package database

import (
	"context"
	"time"

	"github.com/uptrace/bun"
)

// TODO: Cleanup.

/* Shared stuff. */

type User struct {
	bun.BaseModel `bun:"table:users"`

	ID        uint64 `bun:"id, pk"`
	AuthToken string `bun:"auth_token"`
}

type BadgeType uint8

const (
	BadgeNormal BadgeType = iota
	BadgeStaff
)

type Badge struct {
	bun.BaseModel `bun:"table:badges"`

	OwnerID uint64 `bun:"owner_id" json:"-"`

	Type BadgeType `bun:"badge_type" json:"type"`

	Icon        string `bun:"badge_icon" json:"icon"`
	Name        string `bun:"badge_name" json:"name"`
	Description string `bun:"badge_description" json:"description"`
	RedirectURL string `bun:"redirect_url" json:"redirect_url"`
}

/* StupidityDB stuff. */

type StupidityVote struct {
	bun.BaseModel `bun:"table:stupidity_votes"`

	RaterID uint64 `bun:"rater_id"`
	Rating  uint8  `bun:"rating"`

	RatedID uint64 `bun:"rated_id"`
}

/* ReviewDB stuff. */

type ReviewType uint8

const (
	ReviewNormal ReviewType = iota
	ReviewSystem
)

type Review struct {
	bun.BaseModel `bun:"table:reviews"`

	// ID of the review.
	ID        uint32     `bun:"id, pk, autoincrement" json:"id"`
	Type      ReviewType `bun:"type" json:"type"`
	Stars     uint32     `bun:"stars" json:"stars"`
	Content   string     `bun:"content" json:"content"`
	Timestamp time.Time  `bun:"timestamp, default:current_timestamp" json:"timestamp"`

	ReviewerID uint64 `bun:"reviewer_id" json:"reviewer_id"`
	ReviewedID uint64 `bun:"reviewed_id" json:"-"`
}

type UserReviewsUser struct {
	bun.BaseModel `bun:"table:ur_users"`

	ID           int32       `bun:"id,pk,autoincrement" json:"ID"`
	DiscordID    string      `bun:"discordid,type:numeric" json:"discordID"`
	Token        string      `bun:"token" json:"-"`
	Username     string      `bun:"username" json:"username"`
	UserType     int32       `bun:"column:type" json:"-"`
	ProfilePhoto string      `bun:"profile_photo" json:"profilePhoto"`
	ClientMod    string      `bun:"client_mod" json:"clientMod"`
	WarningCount int32       `bun:"warning_count" json:"warningCount"`
	BanEndDate   time.Time   `bun:"ban_end_date" json:"banEndDate"`
	Badges       []UserBadge `bun:"-" json:"badges"`
}

type AdminUser struct {
	bun.BaseModel `bun:"table:ur_users"`
	DiscordID     string `bun:"discordid,type:numeric"`
	ProfilePhoto  string `bun:"profile_photo"`
}

type ReviewReport struct {
	bun.BaseModel `bun:"table:ur_reports"`

	ID         int32 `bun:"id,pk,autoincrement"`
	UserID     int32 `bun:"userid"`
	ReviewID   int32 `bun:"reviewid"`
	ReporterID int32 `bun:"reporterid"`
}

type UserBadgeLegacy struct {
	bun.BaseModel `bun:"table:userbadges"`

	ID               int32  `bun:"id,pk,autoincrement" json:"-"`
	DiscordID        string `bun:"discordid,type:numeric" json:"-"`
	BadgeName        string `bun:"badge_name" json:"badge_name"`
	BadgeIcon        string `bun:"badge_icon" json:"badge_icon"`
	RedirectURL      string `bun:"redirect_url" json:"redirect_url"`
	BadgeType        int32  `bun:"badge_type" json:"badge_type"`
	BadgeDescription string `bun:"badge_description" json:"badge_description"`
}

type ActionLog struct {
	bun.BaseModel `bun:"table:actionlog"`

	Action string `bun:"action" json:"action"`

	ReviewID     int32  `bun:"id,pk,autoincrement" json:"id"`
	UserID       int64  `bun:"userid,type:numeric" json:"-"`
	SenderUserID int32  `bun:"senderuserid" json:"senderuserid"`
	Comment      string `bun:"comment" json:"comment"`

	UpdatedString string `bun:"updatedstring"`
	ActionUserID  int32  `bun:"actionuserid"`
}

func createSchemas() error {
	models := []any{
		(*StupitStat)(nil),
		(*UserInfo)(nil),
		(*UserReview)(nil),
		(*UserReviewsUser)(nil),
		(*ReviewReport)(nil),
		(*UserBadgeLegacy)(nil),
		(*ActionLog)(nil),
	}

	for _, model := range models {
		if _, err := DB.NewCreateTable().IfNotExists().Model(model).Exec(context.Background()); err != nil {
			return err
		}
	}

	return nil
}
