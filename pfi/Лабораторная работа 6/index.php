<?php
declare(strict_types=1);

require_once __DIR__ . '/connection.php';

$message = '';
$errorMessage = '';
$searchTerm = '';
$rows = [];
$searchStatement = null;

try {
    $connection = create_connection();

    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        if (isset($_POST['add_new'])) {
            $surname = trim((string) ($_POST['surname'] ?? ''));
            $sport = trim((string) ($_POST['sport'] ?? ''));

            if ($surname === '' || $sport === '') {
                $errorMessage = 'Заполните фамилию и вид спорта.';
            } else {
                $insertStatement = $connection->prepare(
                    'INSERT INTO sportsmen (surname, sport) VALUES (?, ?)'
                );
                $insertStatement->bind_param('ss', $surname, $sport);
                $insertStatement->execute();
                $insertStatement->close();

                $message = 'Новая запись добавлена.';
            }
        }

        if (isset($_POST['search'])) {
            $searchTerm = trim((string) ($_POST['search_term'] ?? ''));
        }
    }

    if ($searchTerm !== '') {
        $pattern = '%' . $searchTerm . '%';
        $searchStatement = $connection->prepare(
            'SELECT id, surname, sport, created_at
             FROM sportsmen
             WHERE surname LIKE ? OR sport LIKE ?
             ORDER BY id DESC'
        );
        $searchStatement->bind_param('ss', $pattern, $pattern);
        $searchStatement->execute();
        $result = $searchStatement->get_result();
    } else {
        $result = $connection->query(
            'SELECT id, surname, sport, created_at
             FROM sportsmen
             ORDER BY id DESC'
        );
    }

    while ($row = $result->fetch_assoc()) {
        $rows[] = $row;
    }

    if ($searchStatement instanceof mysqli_stmt) {
        $searchStatement->close();
    }

    $connection->close();
} catch (Throwable $exception) {
    $errorMessage = 'Не удалось подключиться к базе данных. Сначала выполните init.sql, затем обновите страницу. Техническая ошибка: ' . $exception->getMessage();
}
?>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Лабораторная работа 6</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<main class="page">
    <section class="card hero">
        <p class="eyebrow">Лабораторная работа № 6</p>
        <h1>Список спортсменов</h1>
        <p class="lead">
            Веб-приложение для добавления записей в базу данных и поиска по заданному критерию.
        </p>
    </section>

    <section class="grid">
        <form class="card form-card" method="post">
            <h2>Добавить запись</h2>
            <label for="surname">Фамилия спортсмена</label>
            <input id="surname" name="surname" type="text" maxlength="100" required>

            <label for="sport">Вид спорта</label>
            <input id="sport" name="sport" type="text" maxlength="100" required>

            <button type="submit" name="add_new">Добавить</button>
        </form>

        <form class="card form-card" method="post">
            <h2>Поиск</h2>
            <label for="search_term">Фамилия или вид спорта</label>
            <input
                id="search_term"
                name="search_term"
                type="text"
                maxlength="100"
                value="<?= htmlspecialchars($searchTerm, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') ?>"
                placeholder="Например, футбол или Иванов"
            >

            <button type="submit" name="search">Найти</button>
        </form>
    </section>

    <?php if ($message !== ''): ?>
        <div class="status success"><?= htmlspecialchars($message, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') ?></div>
    <?php endif; ?>

    <?php if ($errorMessage !== ''): ?>
        <div class="status error"><?= htmlspecialchars($errorMessage, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') ?></div>
    <?php endif; ?>

    <section class="card table-card">
        <div class="table-header">
            <h2>Список спортсменов</h2>
            <p>
                <?php if ($searchTerm !== ''): ?>
                    Показаны результаты по запросу "<?= htmlspecialchars($searchTerm, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') ?>"
                <?php else: ?>
                    Показаны все записи
                <?php endif; ?>
            </p>
        </div>

        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Фамилия</th>
                    <th>Вид спорта</th>
                    <th>Дата добавления</th>
                </tr>
            </thead>
            <tbody>
                <?php if ($rows === []): ?>
                    <tr>
                        <td colspan="4">По запросу ничего не найдено.</td>
                    </tr>
                <?php else: ?>
                    <?php foreach ($rows as $row): ?>
                        <tr>
                            <td><?= (int) $row['id'] ?></td>
                            <td><?= htmlspecialchars($row['surname'], ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') ?></td>
                            <td><?= htmlspecialchars($row['sport'], ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') ?></td>
                            <td><?= htmlspecialchars($row['created_at'], ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') ?></td>
                        </tr>
                    <?php endforeach; ?>
                <?php endif; ?>
            </tbody>
        </table>
    </section>
</main>
</body>
</html>
