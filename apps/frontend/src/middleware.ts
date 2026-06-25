import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const token = request.cookies.get("access_token")?.value;
  const role = request.cookies.get("user_role")?.value;

  const isAuthRoute = pathname.startsWith("/auth");
  const isAuthenticated = !!token;

  // Authenticated user trying to access login → redirect to dashboard
  if (isAuthRoute && isAuthenticated && role) {
    const redirectMap: Record<string, string> = {
      employee: "/employee/dashboard",
      manager: "/manager/dashboard",
      administrator: "/admin/dashboard",
    };
    return NextResponse.redirect(new URL(redirectMap[role] ?? "/", request.url));
  }

  // Unauthenticated user trying to access protected route → redirect to login
  if (!isAuthRoute && !isAuthenticated) {
    return NextResponse.redirect(new URL("/auth/login", request.url));
  }

  // Role-based route protection
  if (isAuthenticated && role) {
    if (pathname.startsWith("/admin") && role !== "administrator") {
      return NextResponse.redirect(new URL("/auth/login", request.url));
    }
    if (pathname.startsWith("/manager") && !["manager", "administrator"].includes(role)) {
      return NextResponse.redirect(new URL("/auth/login", request.url));
    }
    if (pathname.startsWith("/employee") && !["employee", "administrator"].includes(role)) {
      return NextResponse.redirect(new URL("/auth/login", request.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|api).*)",
  ],
};
