from random_coffee_be.repositories.user_club_repository import UserClubRepository

class UserClubService:
    def __init__(self, user_club_repository: UserClubRepository):
        self.user_club_repository = user_club_repository

    async def join_club(self, user_id: int, club_id: int):
        await self.user_club_repository.join_club(user_id, club_id)

    async def leave_club(self, user_id: int, club_id: int):
        await self.user_club_repository.leave_club(user_id, club_id)