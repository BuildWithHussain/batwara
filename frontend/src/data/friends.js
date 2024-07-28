import { createResource } from "frappe-ui";
import { sessionUser } from "./session";

export function getFriendsListResource() {
	return createResource({
		url: "batwara.api.get_friends_for_current_user",
		cache: "friends-list",
		auto: sessionUser() && sessionUser() != "Guest"
	})
}


