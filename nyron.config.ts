import { defineConfig } from "@nyron/cli/config"

export default defineConfig({
  repo: "v0id-user/coin",
  projects: {
    coin: {
      tagPrefix: "coin@",
      path: "__version__/",
    },
  },
  autoChangelog: true,
  onPushReminder: true,
})
