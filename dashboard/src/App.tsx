import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { RouterProvider } from "react-router-dom";
import { router } from "./router";
import { Header } from "./components/layout/Header";
import { Sidebar } from "./components/layout/Sidebar";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-slate-50 text-slate-900">
        <Header />
        <div className="flex">
          <Sidebar />
          <main className="flex-1 p-6">
            <RouterProvider router={router} />
          </main>
        </div>
      </div>
    </QueryClientProvider>
  );
}
