/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    unoptimized: true,
    remotePatterns: [
      { protocol: "https", hostname: "img.youtube.com" },
      { protocol: "https", hostname: "via.placeholder.com" },
    ],
  },
  // Allow dev access from the server's public IP so /_next assets load without CORS warnings.
  allowedDevOrigins: ["http://210.79.128.192:3000"],
};

module.exports = nextConfig;
