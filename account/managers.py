# from django.contrib.auth.models import UserManager
# from common.utils import DataValidationError


# class CustomUserManager(UserManager):

#     def get_or_raise(self, user_id):
#         try:
#             return self.get(id=user_id)
#         except self.model.DoesNotExist:
#             raise DataValidationError(
#                 'User with id %d does not exists' % user_id)
