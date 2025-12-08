module.exports = {
  apps: [
    {
      name: "gravix",
      script: "npm",
      args: "start",
      cwd: "/var/www/gravix-app",
      env: {
        NODE_ENV: "production",
        PORT: "3000",
      },
      watch: false,
      max_restarts: 5,
      restart_delay: 2000,
    },
  ],
};
