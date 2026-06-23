export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh" }}>
      <main style={{ width: "100%", maxWidth: "400px", padding: "2rem" }}>
        {children}
      </main>
    </div>
  );
}
