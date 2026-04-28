// how to run: pytest frontend / Tests / student.test.jsx
// go to frontend folder and run "npx vitest"
import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import StudentsTable from "../src/components/Admin/StudentsTable/StudentsTable";

global.fetch = vi.fn(() =>
    Promise.resolve({ ok: true, json: () => Promise.resolve({}) })
);

window.confirm = vi.fn(() => true);

test("renders student list", () => {
  render(
    <MemoryRouter>
      <StudentsTable students={[
        {
          id: 1,
          name: "Ana Costa",
          email: "ana@test.com",
          phone: "123",
          course: "Beginner A1-A2",
          status: "Active"
        }
      ]} />
    </MemoryRouter>
  );

  expect(screen.getByText("Ana Costa")).toBeInTheDocument();
});

test("delete student triggers API call", async () => {
    render(
        <MemoryRouter>
            <StudentsTable students={[{
                id: 1,
                name: "Ana",
                email: "a",
                phone: "b",
                course: "Beginner A1-A2",
                status: "Active"
            }]} />
        </MemoryRouter>
    );

    const deleteBtn = screen.getByText("Delete");

    fireEvent.click(deleteBtn);

    expect(fetch).toHaveBeenCalledWith("/api/students/1", {
        method: "DELETE"
    });
});

test("opens schedule page when clicking schedule", async () => {
    global.fetch = vi.fn()
        .mockResolvedValueOnce({
            json: async () => [{ id: 1, name: "Teacher", course: "Beginner A1-A2" }]
        })
        .mockResolvedValueOnce({
            json: async () => [{ id: 1, day: "Monday", start: "10:00", end: "11:00" }]
        });

    render(
        <MemoryRouter>
            <StudentsTable students={[{
                id: 1,
                name: "Ana",
                email: "a",
                phone: "b",
                course: "Beginner A1-A2",
                status: "Active"
            }]} />
        </MemoryRouter>
    );

    fireEvent.click(screen.getByText("Schedule Course"));

    expect(await screen.findByText("Schedule Classes")).toBeInTheDocument();
});

test("confirm booking sends request", async () => {
    global.fetch = vi.fn()
        .mockResolvedValueOnce({
            json: async () => [{ id: 1, name: "Teacher", course: "Beginner A1-A2" }]
        })
        .mockResolvedValueOnce({
            json: async () => [{ id: 10, day: "Monday", start: "10", end: "11" }]
        })
        .mockResolvedValueOnce({ ok: true });

    render(
        <MemoryRouter>
            <StudentsTable students={[{
                id: 1,
                name: "Ana",
                email: "a",
                phone: "b",
                course: "Beginner A1-A2",
                status: "Active"
            }]} />
        </MemoryRouter>
    );

    fireEvent.click(screen.getByText("Schedule Course"));

    const slotBtn = await screen.findByText(/Monday/);
    fireEvent.click(slotBtn);

    fireEvent.click(screen.getByText("Confirm Booking"));

    expect(fetch).toHaveBeenLastCalledWith("/api/bookings", expect.any(Object));
});