#include <dbus/dbus-glib.h>
$$OBJECT_HEADERS$$

static DBusGConnection *bus;

int main(int argc, const char *argv[])
{
	GMainLoop *mainloop;
	DBusGProxy *proxy;
	GError *error = NULL;
	guint ret;

	g_type_init();
	bus = dbus_g_bus_get(DBUS_BUS_$$SERVICE_TYPE_U$$, &error);
	if (bus == NULL)
		g_error("connect to dbus failed: %s", error->message);

	proxy = dbus_g_proxy_new_for_name(bus, DBUS_SERVICE_DBUS,
			DBUS_PATH_DBUS, DBUS_INTERFACE_DBUS);
	if (!dbus_g_proxy_call(proxy, "RequestName", &error,
				G_TYPE_STRING, "$$SERVICE$$",
				G_TYPE_UINT, 0,
				G_TYPE_INVALID,
				G_TYPE_UINT, &ret,
				G_TYPE_INVALID))
		g_error("unable to register service: %s", error->message);
	if (ret != DBUS_REQUEST_NAME_REPLY_PRIMARY_OWNER)
		g_error("service is already running");

$$INIT_OBJECTS$$

	mainloop = g_main_loop_new(NULL, FALSE);
	g_main_loop_run(mainloop);

	return 0;
}
