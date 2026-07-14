import { useEffect, useState } from "react";
import { deleteHabit, getHabitStrength, skipHabit, getTodayStatus, getHabitHistory } from "../api/habitsApi";
import { Link } from "react-router-dom";

function HabitCard({ habit, onComplete, onDelete }) {
    const [strength, setStrength] = useState(null);
    const [todayStatus, setTodayStatus] = useState(null);
    const [history, setHistory] = useState(null);

    useEffect(() => {
        const fetchHabitStrength = async () => {
            const habitStrength = await getHabitStrength(habit.id);
            const today = new Date().toISOString().slice(0, 10);
            const todayStatusData = await getTodayStatus(habit.id, today);
            setStrength(habitStrength.strength);
            setTodayStatus(todayStatusData.status);
        };

        fetchHabitStrength();
    }, [habit.id]);

    const fetchHabitHistory = async () => {
        if (history !== null) {
            setHistory(null);
            return;
        }
            const historyData = await getHabitHistory(habit.id);
            setHistory(historyData);
        };

    const handleDelete = async () => {
    await deleteHabit(habit.id);
    onDelete(habit.id);
};
  return (
    <div>
      <Link to={`/habits/${habit.id}`}>
         <h3>{habit.name}</h3>
      </Link>
      
        Strength: {strength === null ? "Loading..." : strength}
        {todayStatus === "completed" && <p>Completed today</p>}
        {todayStatus === "skipped" && <p>Skipped today</p>}
      
      <button onClick={handleDelete}>Delete</button>
      <button onClick={async () => {await onComplete(habit.id);
                                    setTodayStatus("completed");
              const habitStrength = await getHabitStrength(habit.id);
        setStrength(habitStrength.strength);}}>Complete</button>
      <button onClick={async () => {await skipHabit(habit.id, new Date().toISOString().slice(0, 10));
                                    setTodayStatus("skipped");
              const habitStrength = await getHabitStrength(habit.id);
        setStrength(habitStrength.strength);}}>Skip</button>
      <button onClick={fetchHabitHistory}>{history === null ? "Show History" : "Hide History"}</button>
        
        {Array.isArray(history) && (
          <div>
            <h4>History</h4>

            {history.map((item) => (
                <p key={item.day}>
                  📅 {item.day}{" "}
                  {item.status === "done" ? "✅ Done" : "⏭️ Skipped"}
                </p>
           ))}
          </div>
        )}
    </div>
  )}

export default HabitCard;