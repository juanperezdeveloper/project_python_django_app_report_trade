<?php

$time = (string)time();
$secret = '&P#L2$Ls~R>wz-jQlldv3V\Eo~h';
$encoded = base64_encode($time);
$hashed = hash('sha256', $time . $secret);

$user = $modx->user;
$profile = $user->getOne('Profile');
$groupMembers = $user->getMany('UserGroupMembers');

$paid = 'trial'; // Assume Trial
foreach ($groupMembers as $groupMember)
{
  if ($groupMember->getOne('UserGroup')-> name == 'member-paid')
  {
    $paid = 'paid';
    break;
  }
}

$form = "<form action='http://www.app.mldraft.com' method='post' target='_blank'>";
$form .= "<input type='hidden' name='encoded' value='" . $encoded . "'/>";
$form .= "<input type='hidden' name='hashed' value='" . $hashed . "'/>";

$form .= "<input type='hidden' name='id' value='" . $user->id . "'/>";
$form .= "<input type='hidden' name='username' value='" . $user->username . "'/>";

$form .= "<input type='hidden' name='fullname' value='" . $profile->fullname . "'/>";
$form .= "<input type='hidden' name='paid' value='" . $paid . "'/>";

$form .= "<input type='submit' value='Go to App' />";
$form .= "</form>";

return $form;