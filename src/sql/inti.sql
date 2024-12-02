CREATE TABLE IF NOT EXISTS soccer_matches (
    id SERIAL PRIMARY KEY,
    sport_id INT NOT NULL,
    league_id INT NOT NULL,
    season_id INT NOT NULL,
    stage_id INT NOT NULL,
    group_id INT,
    aggregate_id INT,
    round_id INT NOT NULL,
    state_id INT NOT NULL,
    venue_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    starting_at TIMESTAMP,
    result_info VARCHAR(100),
    leg VARCHAR(50) NOT NULL,
    details TEXT,
    length INT NOT NULL,
    placeholder BOOLEAN NOT NULL DEFAULT FALSE,
    has_odds BOOLEAN NOT NULL DEFAULT FALSE,
    has_premium_odds BOOLEAN NOT NULL DEFAULT FALSE,
    starting_at_timestamp BIGINT NOT NULL,
    FOREIGN KEY (sport_id) REFERENCES sports(id),
    FOREIGN KEY (league_id) REFERENCES leagues(id),
    FOREIGN KEY (season_id) REFERENCES seasons(id),
    FOREIGN KEY (stage_id) REFERENCES stages(id),
    FOREIGN KEY (round_id) REFERENCES rounds(id),
    FOREIGN KEY (state_id) REFERENCES states(id),
    FOREIGN KEY (venue_id) REFERENCES venues(id)
);

CREATE INDEX idx_league_id ON soccer_matches (league_id);
CREATE INDEX idx_season_id ON soccer_matches (season_id);
CREATE INDEX idx_starting_at_timestamp ON soccer_matches (starting_at_timestamp);
