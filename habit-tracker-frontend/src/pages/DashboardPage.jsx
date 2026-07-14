import Navbar from "../components/Navbar";
import { useEffect, useState } from "react";
import { getHabits, createHabit, completeHabit } from "../api/habitsApi";
import HabitCard from "../components/HabitCard";

function DashboardPage() {
  const [habits, setHabits] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
useEffect(() => {
    const fetchHabits = async () => {
      setIsLoading(true);
      try {
        const habitsData = await getHabits();
        setHabits(habitsData);
      } catch (error) {
        console.error("Error fetching habits:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchHabits();
  }, []);

     const handleAddHabit = async () => {
        const name = prompt("Habit name:");
        const targetPerWeek = prompt("Target per week:");

        if (!name) {
            return;
        }

        const newHabit = await createHabit({ name, target_per_week:Number(targetPerWeek) });
        setHabits([...habits, newHabit]);
    };
    const handleCompleteHabit = async (habitId) => {
        const today = new Date().toISOString().slice(0, 10);

        await completeHabit(habitId, today);

        alert("Habit completed!");
};
  if (isLoading) {
    return <p>Loading...</p>;
  }

  return (
    <>
      <Navbar />

      <main>
        <h1>My Habits</h1>

        <button onClick={handleAddHabit}>Add Habit</button>

        <section>
            {isLoading ? (
               <p>Loading habits...</p>
            ) : habits.length === 0 ? (
                <p>No habits yet</p>
            ) : (
                habits.map((habit) => (
                    <HabitCard key={habit.id} habit={habit}
                     onComplete={handleCompleteHabit}
                     onDelete={(habitId) => {
                setHabits(habits.filter((habit) => habit.id !== habitId));
                    }}
                />
                ))
            )}
        </section>
      </main>
    </>
  );
}

export default DashboardPage;