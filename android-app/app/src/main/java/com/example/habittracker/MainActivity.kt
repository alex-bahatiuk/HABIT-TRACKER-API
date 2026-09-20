package com.example.habittracker
import com.example.habittracker.ui.LoginScreen
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.safeDrawingPadding
import com.example.habittracker.ui.theme.HabitTrackerTheme
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import com.example.habittracker.model.GoalCategory
import com.example.habittracker.ui.RegisterScreen
import com.example.habittracker.ui.WelcomeScreen
import com.example.habittracker.ui.HabitSelectionScreen
import com.example.habittracker.ui.HomeScreen
import com.example.habittracker.ui.SetupScreen
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.habittracker.viewmodel.RegisterViewModel
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.safeDrawingPadding
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            HabitTrackerTheme {
                Box(
                    modifier = Modifier.fillMaxSize().safeDrawingPadding()
                )

                    var currentScreen by remember {
                        mutableStateOf("welcome")
                    }

                        var selectedGoal by remember { mutableStateOf<GoalCategory?>(null) }
                        val registerViewModel: RegisterViewModel = viewModel()
                        when (currentScreen) {

                            "welcome" -> {
                                WelcomeScreen(
                                    onNextClick = {
                                        currentScreen = "setup"
                                    }
                                )
                        }

                        "setup" -> {
                        SetupScreen(
                            onNextClick = {
                                currentScreen = "habits"
                            }
                        )
                    }

                        "habits" -> {
                        HabitSelectionScreen(
                            onNextClick = {
                                currentScreen = "login"
                            }
                        )
                    }

                        "login" -> {
                        LoginScreen(
                            onRegisterClick = {
                                currentScreen = "register"
                            },
                            onLoginSuccess = { currentScreen = "home" }
                        )
                    }

                        "register" -> {
                        RegisterScreen(
                            onBackToLogin = {
                                currentScreen = "login"
                            },
                            viewModel = registerViewModel
                        )
                    }

                        "home" -> {
                        HomeScreen()
                    }
                    }
                }
            }
        }
    }






