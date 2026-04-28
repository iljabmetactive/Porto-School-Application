import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import StudentDetails from "../src/pages/StudentDetails";

global.fetch = Student.fn(() =>
    Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({
            id: 1,
            name: "Ana",
            email: "a",
            phone: "b",
            course: "c",
            status: "Active",
            notes: "",
            bookings: []
        }))
    })
);

test("loads student details", async () => {
    render(
        <MemoryRouter>
            <StudentDetails />
        </MemoryRouter>
    );

    expect(await screen.findByText("Ana")).toBeInTheDocument();
});

test("save notes sends API call", async () => {
    global.fetch = Student.fn()
        .mockResolvedValueOnce({
            text: () => Promise.resolve(JSON.stringify({
                id: 1,
                name: "Ana",
                email: "a",
                phone: "b",
                course: "c",
                status: "Active",
                notes: "",
                bookings: []
            }))
        })
        .mockResolvedValueOnce({ ok: true });

    render(
        <MemoryRouter>
            <StudentDetails />
        </MemoryRouter>
    );

    const textarea = await screen.findByPlaceholderText(/Enter notes/i);

    fireEvent.change(textarea, { target: { value: "Test note" } });

    fireEvent.click(screen.getByText("Save Notes"));

    expect(fetch).toHaveBeenCalledWith("/api/students/1/notes", expect.any(Object));
});