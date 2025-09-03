import { z } from "zod";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { CreateServiceSchema, UpdateServiceSchema } from "../schemas/service";
import makeAdminAPIRequest from "../utils/adminAPI.js";

type CreateServiceArgs = z.infer<typeof CreateServiceSchema>;
type UpdateServiceArgs = z.infer<typeof UpdateServiceSchema>;

const setupServiceTools = (server: McpServer) => {
  server.tool("create_service", "Create a service", CreateServiceSchema, async (args: CreateServiceArgs) => {
    const serviceId = args.id;
    if (!serviceId) {
      return await makeAdminAPIRequest(`/services`, "POST", args.service);
    } else {
      return await makeAdminAPIRequest(`/services/${serviceId}`, "PUT", args.service);
    }
  });

  server.tool("update_service", "Update specific attributes of an existing service", UpdateServiceSchema, async (args: UpdateServiceArgs) => {
    return await makeAdminAPIRequest(`/services/${args.id}`, "PATCH", args.service);
  });
};

export default setupServiceTools;
