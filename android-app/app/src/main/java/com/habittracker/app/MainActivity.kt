package com.habittracker.app
import com.habittracker.app.ui.LoginScreen
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.safeDrawingPadding
import com.habittracker.app.ui.theme.HabitTrackerTheme
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import com.habittracker.app.model.GoalCategory
import com.habittracker.app.ui.RegisterScreen
import com.habittracker.app.ui.WelcomeScreen
import com.habittracker.app.ui.HabitSelectionScreen
import com.habittracker.app.ui.HomeScreen
import com.habittracker.app.ui.SetupScreen
import androidx.lifecycle.viewmodel.compose.viewModel
import com.habittracker.app.viewmodel.RegisterViewModel

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






