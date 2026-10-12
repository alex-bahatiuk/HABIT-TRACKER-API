package com.habittracker.app.ui

import android.util.Log
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Button
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.runtime.rememberCoroutineScope
import com.habittracker.app.api.ApiClient
import kotlinx.coroutines.launch
import androidx.compose.ui.platform.LocalContext
import com.habittracker.app.utils.TokenManager
import androidx.compose.ui.graphics.Color
import androidx.credentials.CredentialManager
import androidx.credentials.GetCredentialRequest
import androidx.credentials.CustomCredential
import com.google.android.libraries.identity.googleid.GetGoogleIdOption
import com.google.android.libraries.identity.googleid.GoogleIdTokenCredential
import com.habittracker.app.R
import com.habittracker.app.model.GoogleLoginRequest

@Composable
fun LoginScreen(onRegisterClick: () ->
Unit, onLoginSuccess: () -> Unit) {
    var email by remember {
        mutableStateOf("")
    }

    var password by remember {
        mutableStateOf("")
    }

    var loginError by remember {
    mutableStateOf<String?>(null)
    }
    val scope = rememberCoroutineScope()
    val context = LocalContext.current

    val credentialManager = CredentialManager.create(context)

    val googleIdOption = GetGoogleIdOption.Builder()
        .setFilterByAuthorizedAccounts(false)
        .setServerClientId(context.getString(R.string.google_web_client_id))
        .setAutoSelectEnabled(false)
        .build()

    val request = GetCredentialRequest.Builder()
        .addCredentialOption(googleIdOption)
        .build()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(text = "Habit Tracker")

        Spacer(modifier = Modifier.height(24.dp))

        OutlinedTextField(
            value = email,
            onValueChange = { email = it },
            label = {
                Text("Email")
            },
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Email
            ),
            singleLine = true,
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(16.dp))

        OutlinedTextField(
            value = password,
            onValueChange = { password = it },
            label = {
                Text("Password")
            },
            visualTransformation = PasswordVisualTransformation(),
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Password
            ),
            singleLine = true,
            modifier = Modifier.fillMaxWidth()
        )
        loginError?.let { error ->
            Text(
                  text = error,
                   color = Color.Red
        )
      }
        Spacer(modifier = Modifier.height(24.dp))

        Button(
            onClick = {
                scope.launch {
                     try {
                         val response = ApiClient.authApi.login(
                             email = email,
                             password = password
                         )

                         TokenManager.saveToken(
                             context = context,
                             token = response.access_token
                         )

                         println("TOKEN SAVED")
                         onLoginSuccess()
                     } catch (e: Exception) {
                         loginError = "Incorrect email or password"
                         Log.e("LOGIN", "LOGIN ERROR: ${e.message}")
                     }
                }
                      },

            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Login")
        }

        Spacer(modifier = Modifier.height(12.dp))

        Button(
             onClick = {scope.launch {
                 try {
                     val result = credentialManager.getCredential(
                         context = context,
                         request = request
                     )

                     val credential = result.credential

                     if (credential is CustomCredential &&
                         credential.type == GoogleIdTokenCredential.TYPE_GOOGLE_ID_TOKEN_CREDENTIAL
                     ) {
                         val googleCredential =
                             GoogleIdTokenCredential.createFrom(credential.data)

                         val idToken = googleCredential.idToken

                         Log.d("GOOGLE_LOGIN", "Google token received")

                         val response = ApiClient.authApi.googleLogin(
                             GoogleLoginRequest(id_token = idToken)
                         )

                         TokenManager.saveToken(context, response.access_token)

                         onLoginSuccess()
                     }

                 } catch (e: Exception) {
                     Log.e("GOOGLE_LOGIN", "Google login error: ${e.message}")
                 }
             }
                       },
             modifier = Modifier.fillMaxWidth()
        ) {
             Text(text = "Continue with Google")
        }

        Button(
            onClick = onRegisterClick,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Register")
        }
    }
}