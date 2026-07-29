import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  devIndicators: false,
  async rewrites() {
    const apiUrl = process.env.NEXT_INTERNAL_API_URL ?? "http://api:8000";
    return [
      {
        source: "/api/v1/:path+",
        destination: `${apiUrl}/api/v1/:path+`,
      },
      {
        source: "/api/v1/:path+/",
        destination: `${apiUrl}/api/v1/:path+/`,
      },
    ];
  },
};

export default nextConfig;
