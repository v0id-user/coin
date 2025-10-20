import { defineConfig } from "@nyron/cli/config"

export default defineConfig({
  repo: "v0id-user/coin",
  projects: {
    sdk: {
      tagPrefix: "@my-package/sdk@",
      path: "packages/sdk",
    },
    service: {
      tagPrefix: "@my-package/service@",
      path: "apps/service",
    },
  },
  autoChangelog: true,
  onPushReminder: true,
})
