import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  devIndicators: false,
  async rewrites() {
    // In production (single-port deploy), NEXT_PUBLIC_API_URL is empty and
    // Next.js proxies /api/v1/* to the api container over the internal Docker network.
    // In local dev, NEXT_PUBLIC_API_URL=http://localhost:8089 is set so the
    // browser calls the API directly — rewrites are skipped when the api-client
    // prefixes the URL with the full host.
    const apiUrl = process.env.NEXT_INTERNAL_API_URL ?? "http://api:8000";
    return [
      {
        source: "/api/v1/:path*",
        destination: `${apiUrl}/api/v1/:path*`,
      },
    ];
  },
};

export default nextConfig;
