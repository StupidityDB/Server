package stupiditydb

import (
	"context"
	"errors"

	"github.com/disgoorg/log"
	"golang.org/x/exp/slices"

	"server-go/config"
	"server-go/database"
)

func getStupidity(userID int64) (stupidity *int8, err error) {
	// Check if user has votes on their profile.
	hasVotesOnProfile, err := database.DB.NewSelect().
		Where("RatedDiscordID = ?", userID).
		Model((*database.StupidityVote)(nil)).
		Exists(context.Background())
	if err != nil {
		return nil, errors.New("an error occurred while checking if the user has votes")
	}
	if !hasVotesOnProfile {
		return nil, nil
	}

	rowsThatVoteForUser, err := database.DB.
		Query("SELECT AVG(Rating) FROM StupidityVotes WHERE RatedID = ?", userID)
	defer func() {
		if err = rowsThatVoteForUser.Close(); err != nil {
			log.Errorf("an error occurred while closing the rows: %v", err)
		}
	}()

	if err != nil {
		return nil, errors.New("an error occurred while getting the average stupidity")
	}

	var averageStupidity *float64

	if err = database.DB.ScanRows(
		context.Background(),
		rowsThatVoteForUser,
		&averageStupidity,
	); err != nil {
		return nil, errors.New("an error occurred while getting the average stupidity")
	}

	averageStupidityInt := int8(*averageStupidity)
	return &averageStupidityInt, nil
}

func voteStupidity(vote *database.StupidityVote) (response *string, err error) {
	if vote.Rating > 10 {
		return nil, errors.New("stupidity must be between 0 and 10")
	}

	if slices.Contains(config.OptedOut, vote.RatedDiscordID) {
		return nil, errors.New("user has opted out")
	}

	result, err := database.DB.NewUpdate().
		Where("RatedDiscordID = ?", vote.RatedDiscordID).
		Where("RaterDiscordId = ?", vote.RaterDiscordID).
		Model(vote).
		Exec(context.Background())
	if err != nil {
		log.Errorf("an error occurred while adding the vote to the database: %v", err)
		return nil, errors.New("an error occured while adding the vote to the database")
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return nil, errors.New("an error occured while adding the vote to the database")
	}

	// Vote was updated as a row was affected.
	if rowsAffected != 0 {
		resp := "updated your vote"
		return &resp, nil
	}

	if _, err = database.DB.NewInsert().Model(vote).Exec(context.Background()); err != nil {
		log.Errorf("an error occurred while adding the vote to the database: %v", err)
		return nil, errors.New("an error occured while adding the vote to the database")
	}

	resp := "successfully voted"
	return &resp, nil
}
