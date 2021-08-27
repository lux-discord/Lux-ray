async def send_error(ctx, message):
	return await ctx.send(message, delete_after=5)

async def send_warning(ctx, message):
	return await ctx.send(message, delete_after=10)

async def send_info(ctx, message):
	return await ctx.send(message, delete_after=3)
