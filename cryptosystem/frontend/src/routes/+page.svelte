<script>
    import Home from "../components/base/Home.svelte";
    import { browser } from "$app/environment";
	import { onMount } from "svelte";
    import { getUser } from "../helper/authentication";

    onMount (() => {
        // initial auth token check
        if (localStorage.getItem("access_token")) {
            getUser()
            .then(response => {
                if (response.status === 401) {
                    localStorage.removeItem('access_token')
                    location.reload();
                }
            });
        }
    });
</script>

<Home />