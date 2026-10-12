package com.habittracker.app.model

data class RegisterRequest(
    val email: String,
    val password: String
)

data class GoogleLoginRequest(
    val id_token: String
)

data class UserResponse(
    val id: Int,
    val email: String
)

data class TokenResponse(
    val access_token: String,
    val token_type: String
)


