Authentication Expressions:
principal: Refers to the principal object (e.g. principal.username).
authentication: Refers to the authentication object (e.g. authentication.authorities).

Authorization Expressions:
hasRole(role): Returns true if the current principal has the specified role.
hasAnyRole(role1, role2, ...): Returns true if the current principal has any of the specified roles.
hasAuthority(authority): Returns true if the current principal has the specified authority.
hasAnyAuthority(authority1, authority2, ...): Returns true if the current principal has any of the specified authorities.
hasIpAddress(ipAddressExpression): Returns true if the request came from the specified IP address or subnet.
permitAll: Always returns true.
denyAll: Always returns false.
isAnonymous(): Returns true if the current principal is anonymous.
isAuthenticated(): Returns true if the current principal is authenticated.
isFullyAuthenticated(): Returns true if the current principal is fully authenticated (i.e. not anonymous and not using remember-me authentication).
isRememberMe(): Returns true if the current principal is using remember-me authentication.

Method Security Expressions:
@PreAuthorize: Defines a pre-authorization check that must pass before the method is invoked.
@PostAuthorize: Defines a post-authorization check that must pass after the method is invoked.
@Secured: Defines a list of roles that are allowed to invoke the method.