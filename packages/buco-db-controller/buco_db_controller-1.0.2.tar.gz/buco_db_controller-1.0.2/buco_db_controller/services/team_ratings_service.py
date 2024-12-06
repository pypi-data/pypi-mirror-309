from buco_db_controller.models.team_ratings import TeamRatings
from buco_db_controller.repositories.team_ratings_repository import TeamRatingsRepository
from buco_db_controller.utils import mappers


class TeamRatingsService:
    def __init__(self):
        self.team_ratings_repository = TeamRatingsRepository()

    def upsert_many_team_ratings(self, team_ratings: list):
        self.team_ratings_repository.upsert_many_team_ratings(team_ratings)

    def insert_team_ratings(self, team_ratings: dict):
        self.team_ratings_repository.insert_team_ratings(team_ratings)

    def get_all_team_ratings(self, season: int) -> TeamRatings:
        response = self.team_ratings_repository.get_team_ratings(season)
        return TeamRatings.from_dict(response)

    def get_team_ratings(self, league_name: str, country: str, season: int) -> dict:
        league_name = f'{league_name}_{country}'

        response = self.team_ratings_repository.get_team_ratings(season)
        leagues = response['data'].keys()
        correspond_league = mappers.find_fuzzy_item(league_name, leagues, threshold=80)
        return response['data'][correspond_league]
