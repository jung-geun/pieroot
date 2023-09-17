<script>
    import { time,elapsed } from '../lib/js/store.js';

    const formatter = new Intl.DateTimeFormat('ko-KR', {
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        hour12: false,
    });
</script>

<h1>This server time is {formatter.format($time)}</h1>
