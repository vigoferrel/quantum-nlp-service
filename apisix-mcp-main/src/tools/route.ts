import { z } from "zod";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import makeAdminAPIRequest from "../utils/adminAPI.js";
import { CreateRouteSchema, UpdateRouteSchema } from "../schemas/route";

type CreateRouteArgs = z.infer<typeof CreateRouteSchema>;
type UpdateRouteArgs = z.infer<typeof UpdateRouteSchema>;

const setupRouteTools = (server: McpServer) => {
  server.tool("create_route", "Create a route", CreateRouteSchema, async (args: CreateRouteArgs) => {
    const routeId = args.id;

    if (routeId) {
      return await makeAdminAPIRequest(`/routes/${routeId}`, "PUT", args.route);
    } else {
      return await makeAdminAPIRequest(`/routes`, "POST", args.route);
    }
  });

  server.tool("update_route", "Update specific attributes of an existing route", UpdateRouteSchema, async (args: UpdateRouteArgs) => {
    return await makeAdminAPIRequest(`/routes/${args.id}`, "PATCH", args.route);
  });
};

export default setupRouteTools;
