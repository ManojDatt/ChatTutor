from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from modules.account.models import Account
from modules.chat.serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Q

class Login(APIView):
	permission_classes = (AllowAny,)
	def post(self,request):
		username = request.data.get('username',None)
		password = request.data.get('password',None)
		if username and password:
			users = Account.objects.filter(username__iexact=username)
			if users.exists() and users.first().check_password(password):
				user_obj = users.first()
				serializer = UserSerializer(user_obj)
				if user_obj.is_active:
					token , created = Token.objects.get_or_create(user=user_obj)
					data_list = {}
					data_list.update(serializer.data)
					data_list.update({"token": token.key})

					return Response({"message": "Login Successfully", "data":data_list, "code": 200})
				else:
					message = "Account is inactive."
					return Response({"message": message , "code": 401, 'data': serializer.data } )
			else:
				message = "Unable to login with given credentials"
				return Response({"message": message , "code": 500, 'data': {}} )
		else:
			message = "Invalid login details."
			return Response({"message": message , "code": 500, 'data': {}})

class AccountList(APIView):
	def get(self, request):
		queryset = Account.objects.filter(Q(is_superuser=False)&~Q(id=request.user.id))
		serializers = UserSerializer(queryset, many=True)
		return Response({'message': 'Account list fetch successfully', 'data': serializers.data, 'code': 200})
		