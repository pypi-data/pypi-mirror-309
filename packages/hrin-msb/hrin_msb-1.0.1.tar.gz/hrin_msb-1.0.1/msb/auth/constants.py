AUTH_REQUEST_TYPE_FIELD_NAME = "auth_type"
AUTH_REQUEST_USER_FIELD_NAME = "user"
AUTH_REQUEST_PASSWORD_FIELD_NAME = "password"

AUTH_REQUEST_TYPE_SSO = "sso"
AUTH_REQUEST_TYPE_LDAP = "ldap"
AUTH_REQUEST_TYPE_CRED = "cred"
AUTH_REQUEST_TYPE_ISR = "isr-token"

AUTH_TOKEN_ACCESS_TYPE_ISR = "isr"
AUTH_TOKEN_ACCESS_TYPE_USER = "user"


class TokenFieldNames:
	ID = "id"
	USER_ID = "userid"
	AUTH_ID = "auth_userid"
	USERNAME = "username"
	IS_VALID = "is_valid"
	SESSION = "session"
	ACCESS_TYPE = "access_type"
	OWNER = "owner"
	IP = "ip"
	ENV = "env"


MSB_JWT_TOKEN_VALIDATOR = "msb.auth.validators.JwtTokenValidator"
MSB_INTRA_SERVICE_REQUEST_VALIDATOR = "msb.auth.validators.IntraServiceRequestValidator"


class TokenConst:
	username_field = "username"
	userid_field = "id"
	user_email_field = "email"

	access_token_validity_config_name = 'JWT_ACCESS_TOKEN_VALIDITY'
	refresh_token_validity_config_name = 'JWT_REFRESH_TOKEN_VALIDITY'
	signing_key_config_name = 'JWT_TOKEN_SIGNING_KEY'
	verification_key_config_name = 'JWT_TOKEN_VERIFY_KEY'
	token_audiance_config_name = 'JWT_TOKEN_AUDIENCE'
	token_issuer_config_name = 'JWT_TOKEN_ISSUER'


class DefaultJwtConfig:
	username_field = "username"
	userid_claim = "id"
	userid_field = "userid"
	user_email_field = "email"
	user_class = "msb.auth.users.TokenUser"
	auth_rule = 'msb.auth.defaults.jwt_user_auth_rule'
	algorithm_hs256 = 'HS256'
	auth_header_types = ('Bearer',)
	auth_header_name = 'HTTP_AUTHORIZATION'
	token_type_claim = 'token_type'
	jti_claim = 'jti'
	access_token_lifetime = 15
	refresh_token_lifetime = 1440
	rotate_refresh_tokens = False
	blacklist_after_rotation = False
	audience = None
	issuer = None


class MsAuthConst:
	AUTH_VALIDATION_USER_VALUE = "token"
	AUTH_VALIDATION_AUTH_TYPE = "ms_sso"


class LdapAuthConst:
	AUTH_VALIDATION_AUTH_TYPE = "ldap"


class RoleConst:
	ADMIN_ROLE_ID = 1
	MANAGER_ROLE_ID = 2
	EMPLOYEE_ROLE_ID = 3
	HR_MANAGER_ROLE_ID = 4
	HR_EMPLOYEE_ROLE_ID = 5
	RESOURCE_MANAGER_ROLE_ID = 6
	FINANCE_MANAGER_ROLE_ID = 7
	FINANCE_EMPLOYEE_ROLE_ID = 8
	OPERATIONS_MANAGER_ROLE_ID = 9
	OPERATIONS_EMPLOYEE_ROLE_ID = 10
	IT_MANAGER_ROLE_ID = 11
	IT_EMPLOYEE_ROLE_ID = 12
	GUEST_ROLE_ID = 13
	CONTRACTOR_ROLE_ID = 14
	APPLICATION_QA_ROLE_ID = 15
	REVIEWER_ROLE_ID = 16
	ARCHITECT_ROLE_ID = 17

	ALL_MANAGER_ROLE_IDS = [
		ADMIN_ROLE_ID,
		MANAGER_ROLE_ID, RESOURCE_MANAGER_ROLE_ID, FINANCE_MANAGER_ROLE_ID,
		HR_MANAGER_ROLE_ID, OPERATIONS_MANAGER_ROLE_ID, IT_MANAGER_ROLE_ID,
	]

	ALL_EMPLOYEE_ROLE_IDS = [
		EMPLOYEE_ROLE_ID, HR_EMPLOYEE_ROLE_ID, FINANCE_EMPLOYEE_ROLE_ID,
		OPERATIONS_EMPLOYEE_ROLE_ID, IT_EMPLOYEE_ROLE_ID, APPLICATION_QA_ROLE_ID, ARCHITECT_ROLE_ID
	]

	ALL_MANAGER_AND_EMPLOYEE_ROLE_IDS = [*ALL_MANAGER_ROLE_IDS, *ALL_EMPLOYEE_ROLE_IDS]

	ALL_USER_ROLE_IDS = [*ALL_MANAGER_AND_EMPLOYEE_ROLE_IDS, GUEST_ROLE_ID, CONTRACTOR_ROLE_ID]


class AccessLevelsConst:
	SELF = 0
	DIRECT_REPORTIES = 1
	ALL_REPORTIES = 2
	ALL_REPORTIES_AND_PEERS = 3
	RESTRICTED_ALL = 4
	ALL = 5
	DB_CHOICES = [
		(SELF, "Self"),
		(DIRECT_REPORTIES, "Direct Reporties"),
		(ALL_REPORTIES, "Direct & Indirect Reporties"),
		(ALL_REPORTIES_AND_PEERS, "Direct,Indirect Reporties & Peers"),
		(RESTRICTED_ALL, "Restricted All"),
		(ALL, "ALL"),
	]


class AccountTypeConst:
	SYS_ACCOUNT = 0
	AD_ACCOUNT = 1
	LOCAL_ACCOUNT = 2
	DB_CHOICES = [
		(SYS_ACCOUNT, 'System account'),
		(AD_ACCOUNT, 'AD account'),
		(LOCAL_ACCOUNT, 'Local account')
	]
