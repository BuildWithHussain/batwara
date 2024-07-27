import { createListResource } from "frappe-ui";
import { sessionUser } from "./session";

export function getFriendsListResource() {
	return createListResource({
		doctype: "Friend Mapping",
		fields: ["b as friend", "b.full_name as full_name", "b.user_image as user_image"
		],
		filters: {
			"a": sessionUser()
		},
		orderBy: "b",
		auto: sessionUser() && sessionUser() != "Guest",
		cache: "friends-list"
	})
}
