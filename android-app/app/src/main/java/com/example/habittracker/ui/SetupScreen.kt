package com.example.habittracker.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.habittracker.R
import com.example.habittracker.model.GoalCategory
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.material3.OutlinedButton

@Composable
fun SetupScreen(
    onNextClick: () -> Unit
) {
    var selectedGoal by remember {
        mutableStateOf<GoalCategory?>(null)
    }
    val goals = listOf(
        GoalCategory.HEALTH,
        GoalCategory.ENERGY,
        GoalCategory.PRODUCTIVITY,
        GoalCategory.MOOD,
        GoalCategory.CONFIDENCE,
        GoalCategory.DISCIPLINE
    )
    BoxWithConstraints(
        modifier = Modifier.fillMaxSize()
    ) {
        val compact = maxHeight < 750.dp

        val verticalPadding = if (compact) 12.dp else 40.dp
        val spaceSmall = if (compact) 8.dp else 16.dp
        val spaceMedium = if (compact) 16.dp else 40.dp
        val iconSize = if (compact) 80.dp else 100.dp

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(
                    horizontal = 32.dp,
                    vertical = verticalPadding
                ),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = stringResource(R.string.setup_title),
                fontSize = if (compact)26.sp else 32.sp,
                fontWeight = FontWeight.Bold,
                textAlign = TextAlign.Center
            )

            Text(
                text = stringResource(R.string.setup_subtitle),
                fontSize = 20.sp,
                textAlign = TextAlign.Center,
                color = Color.Gray
            )


            Spacer(modifier = Modifier.height(spaceMedium))

            Box(
                modifier = Modifier
                    .size(iconSize)
                    .background(
                        color = Color(0xFFD8F7E3),
                        shape = RoundedCornerShape(24.dp)
                    ),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    painter = painterResource(R.drawable.outline_checklist_24),
                    contentDescription = null,
                    modifier = Modifier.size(64.dp),
                    tint = Color(0xFF78B82A)
                )
            }

            goals.forEach { goal ->

                GoalButton(
                    text = stringResource(goal.titleRes),
                    selected = selectedGoal == goal,
                    onClick = {
                        selectedGoal = goal
                    }
                )

                Spacer(modifier = Modifier.height(10.dp))
            }

            Spacer(modifier = Modifier.height(20.dp))

            Text(
                text = stringResource(R.string.setup_main_text),
                fontSize = 19.sp,
                textAlign = TextAlign.Center,
                color = Color.Gray
            )

            Spacer(modifier = Modifier.height(spaceMedium))

            Button(
                onClick = {
                    if (selectedGoal != null) {
                        onNextClick()
                    }
                },
                enabled = selectedGoal != null,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(
                    text = stringResource(R.string.next),
                    fontSize = 18.sp
                )
            }
        }
    }
}
@Composable
private fun GoalButton(
    text: String,
    selected: Boolean,
    onClick: () -> Unit
) {
    if (selected) {
        Button(
            onClick = onClick,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text(text = text)
        }
    } else {
        OutlinedButton(
            onClick = onClick,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text(text = text)
        }
    }
}