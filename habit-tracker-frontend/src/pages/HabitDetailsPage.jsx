import { useParams } from "react-router-dom";
import { getHabit, getHabitStats } from "../api/habitsApi";
import { useEffect, useState } from "react";

function HabitDetailsPage() {
    const { id } = useParams();
    const [habit, setHabit] = useState(null);
    const [stats, setStats] = useState(null);

    useEffect(() => {
        const fetchHabit = async () => {
            const habitData = await getHabit(id);
            setHabit(habitData);
        };

        const fetchHabitStats = async () => {
            const statsData = await getHabitStats(id);
            setStats(statsData);
        };

        fetchHabit();
        fetchHabitStats();
    }, [id]);

  if (!habit) {
    return <p>Loading...</p>;
}

   return (
        <div>
            <h1>{habit.name}</h1>
            <p>
               Target per week:{" "}
               {habit.target_per_week ?? "Not set"}
            </p>
            {stats && (
                <>
                    <p>This week: {stats.checked_this_week} / {habit.target_per_week}</p>
                    <p>Weekly streak: {stats.streak} week 
                        {stats.streak !== 1 ? "s" : ""}
                    </p>
                </>
            )}
        </div>
   );}

export default HabitDetailsPage;