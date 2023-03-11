from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        if request.session["user_type"] == "is_customer":
            user.is_customer = True
        elif request.session["user_type"] == "is_worker":
            user.is_worker = True

        if commit:
            user.save()

        return user
