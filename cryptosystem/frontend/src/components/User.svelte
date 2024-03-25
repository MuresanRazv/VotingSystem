<script>
    import user from "../stores/user";
</script>

<h1>User</h1>

{#if $user}
    <p>Welcome {$user.username}!</p>
{/if}