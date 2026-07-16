import { useParams } from "react-router-dom";
import { getHabit, getHabitStats, getHabitHistory } from "../api/habitsApi";
import { useEffect, useState } from "react";
import "./HabitDetailsPage.css";

function HabitDetailsPage() {
    const { id } = useParams();
    const [habit, setHabit] = useState(null);
    const [stats, setStats] = useState(null);
    const [history, setHistory] = useState([]);

    useEffect(() => {
        const fetchHabit = async () => {
            const habitData = await getHabit(id);
            setHabit(habitData);
        };

        const fetchHabitStats = async () => {
            const statsData = await getHabitStats(id);
            setStats(statsData);
        };

        const fetchHabitHistory = async () => {
            const historyData = await getHabitHistory(id);
            setHistory(historyData);
        };

        fetchHabit();
        fetchHabitStats();
        fetchHabitHistory();
    }, [id]);

  if (!habit) {
    return <p>Loading...</p>;
}
const progress =
  habit.target_per_week && stats
    ? Math.min(
        (stats.checked_this_week / habit.target_per_week) * 100,
        100
      )
    : 0;
   return (
        <main className="habit-details-page">
          <section className="habit-details-card">
            <h1>{habit.name}</h1>
            {stats && (<>
                    <div className="info-box">
                        <h3>🎯 Target</h3>
                        <p>{habit.target_per_week ? `${habit.target_per_week} times / week` : "No weekly target"}</p>
                    </div>

            <div className="info-box">
                <h3>📅 This week</h3>
            <p>{habit.target_per_week ? `${stats.checked_this_week} / ${habit.target_per_week}`
             : `${stats.checked_this_week} completions`}</p>
            <div className="progress-bar">

            <div className="progress-fill"
                style={{
                    width: `${progress}%`,
                  }}
                />
            </div>
            </div>

            <div className="info-box">
                <h3>🔥 Weekly streak</h3>
            <p>{stats.streak} week
                 {stats.streak !== 1 ? "s" : ""}
            </p>
            </div>
            </>)}

            <div className="info-box">
                <h3>📆 Recent history</h3>

                {Array.isArray(history) && history.slice(0, 7).map((item) => (
            <p key={item.day}>
                {item.day} — {item.status}
            </p>
                ))}
            </div>
          </section>
        </main>

)}




export default HabitDetailsPage;