<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" 
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
	<title>
	esmljaos / flexirest / source &mdash; bitbucket.org
</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta name="description" content="Mercurial hosting - we're here to serve." />
	<meta name="keywords" content="mercurial,hg,hosting,bitbucket,esmljaos,The,medium-featured,,flexible,reStructuredText,utility,source,sourcecode,test/test_main_integration.py@acae3099d35e" />
	<link rel="stylesheet" type="text/css" href="http://bitbucket.org/m/css/layout.css?12985842" />
	<link rel="stylesheet" type="text/css" href="http://bitbucket.org/m/css/print.css?12985842" media="print" />
	<link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="Bitbucket" />
	<link rel="icon" href="http://bitbucket.org/m/img/logo_new.png" type="image/png"/>
	<script type="text/javascript" src="http://bitbucket.org/m/js/lib/bundle.180909Sep.js?2152820"></script>
	
	<script type="text/javascript">
		$(document).ready(function() {
			Dropdown.init();
			$(".tooltip").tipsy({gravity:'s'});
		});
	</script>
	<noscript>
		<style type="text/css">
			.dropdown-container-text .dropdown {
				position: static !important;
			}
		</style>
	</noscript>

	<!--[if lt IE 7]>
	<style type="text/css">
	body {
		behavior: url(http://bitbucket.org/m/css/csshover.htc);
	}
	
	#issues-issue pre {
		white-space: normal !important;
	}
	
	.changeset-description {
		white-space: normal !important;
	}
	</style>
	<script type="text/javascript"> 
		$(document).ready(function(){ 
			$('#header-wrapper').pngFix();
			$('#sourcelist').pngFix();
			$('.promo-signup-screenshot').pngFix();
		}); 
	</script>
	<![endif]-->
	
	<link rel="stylesheet" href="http://bitbucket.org/m/css/highlight/emacs.css" type="text/css" />

	
</head>
<body class="">
	<div id="main-wrapper">
		<div id="header-wrapper">
			<div id="header-loggedin">
				<a href="/"><img src="http://bitbucket.org/m/img/logo_myriad.png" alt="Bitbucket" id="header-wrapper-logo" /></a>
				
					
					
						<a href="/esmljaos/">
							<img src="http://bitbucket.org/m/c/photos/2009/Mar/29/cache/jag-tecknad__avatar.jpg" alt="esmljaos" id="userimage" />
						</a>
					

					<div id="header-nav">
						<ul>
							<li><a href="/">Home</a></li>
							<li class="has-dropdown">
								<a href="/repo/all/">Repositories</a> 
								<ul>
									<li><a href="/repo/create/">Create new</a> </li>
									<li class="header-nav-repo-button-new">
											<a href="/repo/all/">All public repositories</a>
									</li>
									<li class="header-nav-repo-segmenter-theirs">
											&ndash; your repositories &ndash;
										</li>
									
										<li class="header-nav-repo">
											<img class="repo-dropdown-indicator" src="http://bitbucket.org/m/img/icons/fugue/lock_disable_unlock.png" />
											<a href="/esmljaos/flexirest/" title="The medium-featured, flexible reStructuredText utility (public repository)">flexirest</a>
										</li>
									
										<li class="">
											<img class="repo-dropdown-indicator" src="http://bitbucket.org/m/img/icons/fugue/lock_disable_unlock.png" />
											<a href="/esmljaos/playlist/" title="Playlist is a Python media play list handler. (public repository)">playlist</a>
										</li>
									
									
								</ul>
							</li>
							<li><a href="/account/">Account</a></li>
							<li>
								<a href="/notifications/" class="inbox-no-messages">Inbox</a>
							</li>
							<li>
								<a href="/plans/">
									Plans
								</a>
							</li>
							<li><a href="/help/">Help</a></li>
							<li><a href="/account/signout/">Log out <small>(esmljaos)</small></a></li>
							<li id="topsearch">
								<form action="/repo/all/">
									<input type="text" name="name" />
								</form>
							</li>
						</ul>
					</div>
				
			</div>
		</div>
		<div id="content-wrapper">
			
			
			

			
			
			
	
	





	<script type="text/javascript" src="http://bitbucket.org/m/js/lib/jquery.cookie.js"></script> <!--REMOVE WHEN NEWER BUNDLE THAN 030309Mar -->
	<script type="text/javascript">
		var date = new Date();
		date.setTime(date.getTime() + (365 * 24 * 60 * 60 * 1000));
		var cookieoptions = { path: '/', expires: date };
		
		$(document).ready(function(){
			$('#toggle-repo-content').click(function(){
				$('#repo-desc-cloneinfo').toggle('fast');
				$('#repo-menu').toggle();
				$('#repo-menu-links-mini').toggle(100);
				$('.repo-desc-description').toggle('fast');
				var avatar_new_width = ($('.repo-avatar').width() == 35) ? 16 : 35;
				$('.repo-avatar').animate({ width: avatar_new_width }, 250);
				
				if ($.cookie('toggle_status') == 'hide') {
					$.cookie('toggle_status', 'show', cookieoptions);
					$(this).css('background-image','url(http://bitbucket.org/m/img/repo-toggle-up.png)');
				} else {
					$.cookie('toggle_status', 'hide', cookieoptions);
					$(this).css('background-image','url(http://bitbucket.org/m/img/repo-toggle-down.png)');
				}
			});
			
			if ($.cookie('toggle_status') == 'hide') {
				$('#toggle-repo-content').css('background-image','url(http://bitbucket.org/m/img/repo-toggle-down.png)');
				$('#repo-desc-cloneinfo').hide();
				$('#repo-menu').hide();
				$('#repo-menu-links-mini').show();
				$('.repo-desc-description').hide();
				$('.repo-avatar').css({ width: '16px' });
			} else {
				$('#toggle-repo-content').css('background-image','url(http://bitbucket.org/m/img/repo-toggle-up.png)');
				$('#repo-desc-cloneinfo').show();
				$('#repo-menu').show();
				$('#repo-menu-links-mini').hide();
				$('.repo-desc-description').show();
				$('.repo-avatar').css({ width: '35px' });
			}
		});
	</script>


<div id="tabs">
	<ul class="ui-tabs-nav">
		<li>
			<a href="/esmljaos/flexirest/overview/"><span>Overview</span></a>
		</li>

		<li>
			<a href="/esmljaos/flexirest/downloads/"><span>Downloads (0)</span></a>
		</li>
		
		

		<li class="ui-tabs-selected">
			
				<a href="/esmljaos/flexirest/src/acae3099d35e/"><span>Source</span></a>
			
		</li>
		
		<li>
			<a href="/esmljaos/flexirest/changesets/"><span>Changesets</span></a>
		</li>

		

		
			
				<li class="ui-tabs-nav-issues">
					<a href="/esmljaos/flexirest/issues/?status=new&amp;status=open"><span>Issues (4) &raquo;</span></a>
					<ul>
						<li><a href="/esmljaos/flexirest/issues/?status=new">New issues</a></li>
						<li><a href="/esmljaos/flexirest/issues/?status=new&amp;status=open">Open issues</a></li>
						<li><a href="/esmljaos/flexirest/issues/?status=resolved&amp;status=invalid&amp;status=duplicate">Closed issues</a></li>
					
							<li><a href="/esmljaos/flexirest/issues/mine/">esmljaos's issues</a></li>
					
						<li><a href="/esmljaos/flexirest/issues/">All issues</a></li>
						<li><a href="/esmljaos/flexirest/issues/query/">Advanced query</a></li>
						<li><a href="/esmljaos/flexirest/issues/new/">Create new issue</a></li>
					</ul>
				</li>
			
		
				
		
			
				<li>
					<a href="/esmljaos/flexirest/admin/"><span>Admin</span></a>
				</li>
			
		
		
		<li class="tabs-right tabs-far-right">
			<a href="/esmljaos/flexirest/descendants/"><span>Forks/Queues (0)</span></a>
		</li>
		
		<li class="tabs-right">
			<a href="/esmljaos/flexirest/zealots/"><span>Followers (1)</span></a>
		</li>
	</ul>
</div>

<div id="repo-menu">
		<div id="repo-menu-links">
			<ul>
				<li>
					<a href="/esmljaos/flexirest/rss/?token=99afdf69714e8fec0477bcca42add5b8" class="noborder repo-menu-rss" title="RSS Feed for flexirest">RSS</a>
				</li>
				<li>
					<a href="/esmljaos/flexirest/atom/?token=99afdf69714e8fec0477bcca42add5b8" class="noborder repo-menu-atom" title="Atom Feed for flexirest">Atom</a>
				</li>
				
				<li>
					<a href="/esmljaos/flexirest/pull/" class="link-request-pull">
						pull request
					</a>
				</li>
				
				<li><a href="/esmljaos/flexirest/fork/" class="link-fork">fork</a></li>
				
					<li><a href="/esmljaos/flexirest/hack/" class="link-hack">patch queue</a></li>
				
				<li>
					
						<a rel="nofollow" href="/esmljaos/flexirest/follow/" class="link-follow follow-xhr following">following</a>
					
				</li>
				<li><a class="link-download">get source &raquo;</a>

					<ul>
						
							<li><a rel="nofollow" href="/esmljaos/flexirest/get/acae3099d35e.zip" class="zip">zip</a></li>
							<li><a rel="nofollow" href="/esmljaos/flexirest/get/acae3099d35e.gz" class="compressed">gz</a></li>
							<li><a rel="nofollow" href="/esmljaos/flexirest/get/acae3099d35e.bz2" class="compressed">bz2</a></li>						
						
					</ul>
				</li>
			</ul>
		</div>
		
		
		<div id="repo-menu-branches-tags">
 			<ul>
				<li class="icon-branches">
					branches &raquo;
					
					<ul>
					
						<li><a href="/esmljaos/flexirest/src/acae3099d35e/">default</a></li>
					
					</ul>
					
				</li>
				<li class="icon-tags">
					tags &raquo;
					
					<ul>
					
						<li><a href="/esmljaos/flexirest/src/acae3099d35e/">tip</a></li>
					
						<li><a href="/esmljaos/flexirest/src/aa94521b9b38/">0.8</a></li>
					
					</ul>
				</li>
			</ul>
		</div>
		
		
		<div class="cb"></div>
	</div>
	<div id="repo-desc" class="layout-box">
		
		
		<div id="repo-menu-links-mini" class="right">
			<ul>
				<li>
					<a href="/esmljaos/flexirest/rss/?token=99afdf69714e8fec0477bcca42add5b8" class="noborder repo-menu-rss" title="RSS Feed for flexirest"></a>
				</li>
				<li>
					<a href="/esmljaos/flexirest/atom/?token=99afdf69714e8fec0477bcca42add5b8" class="noborder repo-menu-atom" title="Atom Feed for flexirest"></a>
				</li>
				
				<li>
					<a href="/esmljaos/flexirest/pull/" class="tooltip noborder link-request-pull" title="Pull request"></a>
				</li>
				
				<li><a href="/esmljaos/flexirest/fork/" class="tooltip noborder link-fork" title="Fork"></a></li>
				
					<li><a href="/esmljaos/flexirest/hack/" class="tooltip noborder link-hack" title="Patch queue"></a></li>
				
				<li><a class="tooltip noborder link-download" title="Get source"></a>

					<ul>
						
							<li><a rel="nofollow" href="/esmljaos/flexirest/get/acae3099d35e.zip" class="zip">zip</a></li>
							<li><a rel="nofollow" href="/esmljaos/flexirest/get/acae3099d35e.gz" class="compressed">gz</a></li>
							<li><a rel="nofollow" href="/esmljaos/flexirest/get/acae3099d35e.bz2" class="compressed">bz2</a></li>						
						
					</ul>
				</li>
			</ul>
		</div>
		
		<h3>
			<a href="/esmljaos/">esmljaos</a> / 
			<a href="/esmljaos/flexirest/">flexirest</a>
			 <span>(<a href="http://www.aspektratio.net/flexirest">http://aspektratio.net/flexirest</a>)</span>
			
		</h3>
		
		
		
		
		
		<p class="repo-desc-description">The medium-featured, flexible reStructuredText utility</p>
		
		<div id="repo-desc-cloneinfo">Clone this repository (size: 90.7 KB): <a href="https://esmljaos@bitbucket.org/esmljaos/flexirest/" onclick="$('#clone-url-ssh').hide();$('#clone-url-https').toggle();return(false);"><small>HTTPS</small></a> / <a href="ssh://hg@bitbucket.org/esmljaos/flexirest/" onclick="$('#clone-url-https').hide();$('#clone-url-ssh').toggle();return(false);"><small>SSH</small></a><br/>
		<pre id="clone-url-https">$ hg clone <a href="https://esmljaos@bitbucket.org/esmljaos/flexirest/">https://esmljaos@bitbucket.org/esmljaos/flexirest/</a></pre>
		
		<pre id="clone-url-ssh" style="display:none;">$ hg clone <a href="ssh://hg@bitbucket.org/esmljaos/flexirest/">ssh://hg@bitbucket.org/esmljaos/flexirest/</a></pre></div>
		
		<div class="cb"></div>
		<a href="#" id="toggle-repo-content"></a>
	</div>


			
			





<div id="source-summary" class="layout-box">
	<div class="right">
		<table>
			<tr>
				<td>commit 91:</td>
				<td>acae3099d35e</td>
			</tr>
			
				<tr>
					<td>parent 90:</td>
					<td>
						<a href="/esmljaos/flexirest/changeset/12a37b836e6a/" title="<b>Author:</b> ja...@medea<br/><b>Age:</b> 3 days ago<br/>Unify minimal fixture." class="tooltip tooltip-ul">12a37b836e6a</a>
					</td>
				</tr>
			
			
			<tr>
				<td>branch: </td>
				<td>default</td>
			</tr>
			
				<tr>
					<td>tags:</td>
					<td>tip</td>
				</tr>
			
		</table>
	</div>

<div class="changeset-description">Pre-run of the latex2pdf smoke test was succesfull! Need to test with style also</div>
	
	<div>
		
			
				
					<img src="http://bitbucket.org/m/img/no_avatar.gif" class="avatar left" alt="" />
				
			
		
			<span>
				
					ja...@medea
				
				<br/>
				<small>3 days ago</small>
			</span>
		
	</div>
				
	<div class="cb"></div>
</div>



<div id="source-path" class="layout-box">
	<a href="/esmljaos/flexirest/src/">flexirest</a> /
	
		
			
				<a href='/esmljaos/flexirest/src/acae3099d35e/test/'>
					test
				</a>
			
		
		/
	
		
			
				test_main_integration.py
			
		
		
	
</div>


<div id="source-view" class="scroll-x">
	<table class="info-table">
		<tr>
			<th>r91:acae3099d35e</th>
			<th>120 loc</th>
			<th>4.0 KB</th>
			<th class="source-view-links">
				<a id="embed-link" href="#" onclick="makeEmbed('#embed-link', 'http://bitbucket.org/esmljaos/flexirest/src/acae3099d35e/test/test_main_integration.py?embed=t');">embed</a> /
				<a href='/esmljaos/flexirest/history/test/test_main_integration.py'>history</a> / 
				<a href='/esmljaos/flexirest/annotate/acae3099d35e/test/test_main_integration.py'>annotate</a> / 
				<a href='/esmljaos/flexirest/raw/acae3099d35e/test/test_main_integration.py'>raw</a> / 
				<form action="/esmljaos/flexirest/diff/test/test_main_integration.py" method="get" class="source-view-form">
					
					<input type="hidden" name="diff2" value="acae3099d35e"/>
						<select name="diff1" class="smaller">
							
								
							
								
									<option value="12a37b836e6a">
										r90:12a37b836e6a
									</option>
								
							
								
									<option value="819d868a7eac">
										r89:819d868a7eac
									</option>
								
							
								
									<option value="1354ea4259c8">
										r88:1354ea4259c8
									</option>
								
							
								
									<option value="cb16ffc22b79">
										r76:cb16ffc22b79
									</option>
								
							
								
									<option value="6b52921fab60">
										r73:6b52921fab60
									</option>
								
							
								
									<option value="42674633ad2f">
										r20:42674633ad2f
									</option>
								
							
								
									<option value="b7fd0213a4df">
										r19:b7fd0213a4df
									</option>
								
							
						</select>
						<input type="submit" value="diff" class="smaller"/>
					
				</form>
			</th>
		</tr>
	</table>
	
		
			<table class="highlighttable"><tr><td class="linenos"><div class="linenodiv"><pre><a href="#cl-1">  1</a>
<a href="#cl-2">  2</a>
<a href="#cl-3">  3</a>
<a href="#cl-4">  4</a>
<a href="#cl-5">  5</a>
<a href="#cl-6">  6</a>
<a href="#cl-7">  7</a>
<a href="#cl-8">  8</a>
<a href="#cl-9">  9</a>
<a href="#cl-10"> 10</a>
<a href="#cl-11"> 11</a>
<a href="#cl-12"> 12</a>
<a href="#cl-13"> 13</a>
<a href="#cl-14"> 14</a>
<a href="#cl-15"> 15</a>
<a href="#cl-16"> 16</a>
<a href="#cl-17"> 17</a>
<a href="#cl-18"> 18</a>
<a href="#cl-19"> 19</a>
<a href="#cl-20"> 20</a>
<a href="#cl-21"> 21</a>
<a href="#cl-22"> 22</a>
<a href="#cl-23"> 23</a>
<a href="#cl-24"> 24</a>
<a href="#cl-25"> 25</a>
<a href="#cl-26"> 26</a>
<a href="#cl-27"> 27</a>
<a href="#cl-28"> 28</a>
<a href="#cl-29"> 29</a>
<a href="#cl-30"> 30</a>
<a href="#cl-31"> 31</a>
<a href="#cl-32"> 32</a>
<a href="#cl-33"> 33</a>
<a href="#cl-34"> 34</a>
<a href="#cl-35"> 35</a>
<a href="#cl-36"> 36</a>
<a href="#cl-37"> 37</a>
<a href="#cl-38"> 38</a>
<a href="#cl-39"> 39</a>
<a href="#cl-40"> 40</a>
<a href="#cl-41"> 41</a>
<a href="#cl-42"> 42</a>
<a href="#cl-43"> 43</a>
<a href="#cl-44"> 44</a>
<a href="#cl-45"> 45</a>
<a href="#cl-46"> 46</a>
<a href="#cl-47"> 47</a>
<a href="#cl-48"> 48</a>
<a href="#cl-49"> 49</a>
<a href="#cl-50"> 50</a>
<a href="#cl-51"> 51</a>
<a href="#cl-52"> 52</a>
<a href="#cl-53"> 53</a>
<a href="#cl-54"> 54</a>
<a href="#cl-55"> 55</a>
<a href="#cl-56"> 56</a>
<a href="#cl-57"> 57</a>
<a href="#cl-58"> 58</a>
<a href="#cl-59"> 59</a>
<a href="#cl-60"> 60</a>
<a href="#cl-61"> 61</a>
<a href="#cl-62"> 62</a>
<a href="#cl-63"> 63</a>
<a href="#cl-64"> 64</a>
<a href="#cl-65"> 65</a>
<a href="#cl-66"> 66</a>
<a href="#cl-67"> 67</a>
<a href="#cl-68"> 68</a>
<a href="#cl-69"> 69</a>
<a href="#cl-70"> 70</a>
<a href="#cl-71"> 71</a>
<a href="#cl-72"> 72</a>
<a href="#cl-73"> 73</a>
<a href="#cl-74"> 74</a>
<a href="#cl-75"> 75</a>
<a href="#cl-76"> 76</a>
<a href="#cl-77"> 77</a>
<a href="#cl-78"> 78</a>
<a href="#cl-79"> 79</a>
<a href="#cl-80"> 80</a>
<a href="#cl-81"> 81</a>
<a href="#cl-82"> 82</a>
<a href="#cl-83"> 83</a>
<a href="#cl-84"> 84</a>
<a href="#cl-85"> 85</a>
<a href="#cl-86"> 86</a>
<a href="#cl-87"> 87</a>
<a href="#cl-88"> 88</a>
<a href="#cl-89"> 89</a>
<a href="#cl-90"> 90</a>
<a href="#cl-91"> 91</a>
<a href="#cl-92"> 92</a>
<a href="#cl-93"> 93</a>
<a href="#cl-94"> 94</a>
<a href="#cl-95"> 95</a>
<a href="#cl-96"> 96</a>
<a href="#cl-97"> 97</a>
<a href="#cl-98"> 98</a>
<a href="#cl-99"> 99</a>
<a href="#cl-100">100</a>
<a href="#cl-101">101</a>
<a href="#cl-102">102</a>
<a href="#cl-103">103</a>
<a href="#cl-104">104</a>
<a href="#cl-105">105</a>
<a href="#cl-106">106</a>
<a href="#cl-107">107</a>
<a href="#cl-108">108</a>
<a href="#cl-109">109</a>
<a href="#cl-110">110</a>
<a href="#cl-111">111</a>
<a href="#cl-112">112</a>
<a href="#cl-113">113</a>
<a href="#cl-114">114</a>
<a href="#cl-115">115</a>
<a href="#cl-116">116</a>
<a href="#cl-117">117</a>
<a href="#cl-118">118</a>
<a href="#cl-119">119</a>
<a href="#cl-120">120</a>
</pre></div></td><td class="code"><div class="highlight"><pre><a name="cl-1"></a><span class="kn">import</span> <span class="nn">os</span>
<a name="cl-2"></a><span class="kn">import</span> <span class="nn">textwrap</span>
<a name="cl-3"></a><span class="kn">import</span> <span class="nn">functools</span>
<a name="cl-4"></a><span class="kn">import</span> <span class="nn">imp</span>
<a name="cl-5"></a><span class="kn">import</span> <span class="nn">shutil</span>
<a name="cl-6"></a><span class="kn">import</span> <span class="nn">tempfile</span>
<a name="cl-7"></a>
<a name="cl-8"></a><span class="kn">from</span> <span class="nn">docutils</span> <span class="kn">import</span> <span class="n">nodes</span>
<a name="cl-9"></a>
<a name="cl-10"></a><span class="kn">from</span> <span class="nn">nose.tools</span> <span class="kn">import</span> <span class="n">assert_equals</span><span class="p">,</span> <span class="n">assert_true</span><span class="p">,</span> <span class="n">with_setup</span><span class="p">,</span> <span class="n">raises</span>
<a name="cl-11"></a>
<a name="cl-12"></a><span class="kn">from</span> <span class="nn">flexirest.tests</span> <span class="kn">import</span> <span class="n">support</span>
<a name="cl-13"></a>
<a name="cl-14"></a><span class="kn">from</span> <span class="nn">flexirest</span> <span class="kn">import</span> <span class="n">main</span>
<a name="cl-15"></a><span class="kn">from</span> <span class="nn">flexirest.tests</span> <span class="kn">import</span> <span class="n">test_tex</span>
<a name="cl-16"></a>
<a name="cl-17"></a><span class="kn">from</span> <span class="nn">StringIO</span> <span class="kn">import</span> <span class="n">StringIO</span>
<a name="cl-18"></a>
<a name="cl-19"></a><span class="c"># XXX Use support.get_minimal_fixture instead!</span>
<a name="cl-20"></a><span class="k">def</span> <span class="nf">get_minimal_fixture</span><span class="p">():</span>
<a name="cl-21"></a>    <span class="k">return</span> <span class="n">StringIO</span><span class="p">(</span><span class="n">textwrap</span><span class="o">.</span><span class="n">dedent</span><span class="p">(</span><span class="s">&quot;&quot;&quot;</span>
<a name="cl-22"></a><span class="s">                                    ======</span>
<a name="cl-23"></a><span class="s">                                    654321</span>
<a name="cl-24"></a><span class="s">                                    ======</span>
<a name="cl-25"></a><span class="s">                                    RST Text</span>
<a name="cl-26"></a><span class="s">                                    &quot;&quot;&quot;</span><span class="p">))</span>
<a name="cl-27"></a>
<a name="cl-28"></a><span class="n">BASIC_TMPL</span> <span class="o">=</span> <span class="s">&#39;/tmp/tmpl_basic.txt&#39;</span>
<a name="cl-29"></a>
<a name="cl-30"></a><span class="n">tmpl_basic_creator</span> <span class="o">=</span> <span class="n">functools</span><span class="o">.</span><span class="n">partial</span><span class="p">(</span><span class="n">support</span><span class="o">.</span><span class="n">create_gc_testfile</span><span class="p">,</span> <span class="n">BASIC_TMPL</span><span class="p">,</span> <span class="n">textwrap</span><span class="o">.</span><span class="n">dedent</span><span class="p">(</span><span class="s">&quot;&quot;&quot;</span>
<a name="cl-31"></a><span class="s">the_template </span><span class="si">%(whole)s</span><span class="s"></span>
<a name="cl-32"></a><span class="s">&quot;&quot;&quot;</span><span class="p">))</span>
<a name="cl-33"></a>
<a name="cl-34"></a><span class="nd">@with_setup</span><span class="p">(</span><span class="n">tmpl_basic_creator</span><span class="p">,</span> <span class="n">support</span><span class="o">.</span><span class="n">clean_gc_testfiles</span><span class="p">)</span>
<a name="cl-35"></a><span class="k">def</span> <span class="nf">test_template_basic</span><span class="p">():</span>
<a name="cl-36"></a>    <span class="n">capture</span> <span class="o">=</span> <span class="n">StringIO</span><span class="p">()</span>
<a name="cl-37"></a>    <span class="n">main</span><span class="o">.</span><span class="n">_import</span> <span class="o">=</span> <span class="k">lambda</span> <span class="n">m</span><span class="p">,</span> <span class="n">r</span><span class="p">:</span> <span class="n">imp</span><span class="o">.</span><span class="n">new_module</span><span class="p">(</span><span class="n">m</span><span class="p">)</span>
<a name="cl-38"></a>    <span class="n">rc</span> <span class="o">=</span> <span class="n">main</span><span class="o">.</span><span class="n">commandline</span><span class="p">([</span><span class="s">&#39;--template=</span><span class="si">%s</span><span class="s">&#39;</span> <span class="o">%</span> <span class="n">BASIC_TMPL</span><span class="p">,</span> <span class="s">&#39;--writer=pseudoxml&#39;</span><span class="p">],</span>
<a name="cl-39"></a>                          <span class="n">source</span><span class="o">=</span><span class="n">get_minimal_fixture</span><span class="p">(),</span> <span class="n">destination</span><span class="o">=</span><span class="n">capture</span><span class="p">)</span>
<a name="cl-40"></a>    <span class="n">out</span> <span class="o">=</span> <span class="n">capture</span><span class="o">.</span><span class="n">getvalue</span><span class="p">()</span>
<a name="cl-41"></a>    <span class="n">assert_true</span><span class="p">(</span><span class="s">&#39;the_template&#39;</span> <span class="ow">in</span> <span class="n">out</span><span class="p">)</span>
<a name="cl-42"></a>    <span class="n">assert_true</span><span class="p">(</span><span class="s">&#39;title=&quot;654321&quot;&#39;</span> <span class="ow">in</span> <span class="n">out</span><span class="p">)</span>
<a name="cl-43"></a>
<a name="cl-44"></a><span class="k">def</span> <span class="nf">role_foo</span><span class="p">(</span><span class="n">role</span><span class="p">,</span> <span class="n">rawtext</span><span class="p">,</span> <span class="n">text</span><span class="p">,</span> <span class="n">lineno</span><span class="p">,</span> <span class="n">inliner</span><span class="p">,</span> <span class="n">options</span><span class="o">=</span><span class="bp">None</span><span class="p">,</span> <span class="n">content</span><span class="o">=</span><span class="p">[]):</span>
<a name="cl-45"></a>    <span class="k">if</span> <span class="n">options</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span>
<a name="cl-46"></a>        <span class="n">options</span> <span class="o">=</span> <span class="p">{}</span>
<a name="cl-47"></a>    <span class="n">node</span> <span class="o">=</span> <span class="n">nodes</span><span class="o">.</span><span class="n">TextElement</span><span class="p">(</span><span class="n">text</span><span class="o">=</span><span class="s">u&#39;ROLESTART_</span><span class="si">%s</span><span class="s">_ROLESTOP&#39;</span> <span class="o">%</span> <span class="n">text</span><span class="p">)</span>
<a name="cl-48"></a>    <span class="k">return</span> <span class="n">node</span><span class="p">,</span> <span class="p">[]</span>
<a name="cl-49"></a>
<a name="cl-50"></a><span class="n">ROLE_TMPL</span> <span class="o">=</span> <span class="s">&#39;/tmp/tmpl_full_role.txt&#39;</span>
<a name="cl-51"></a>
<a name="cl-52"></a><span class="n">tmpl_full_role_creator</span> <span class="o">=</span> <span class="n">functools</span><span class="o">.</span><span class="n">partial</span><span class="p">(</span><span class="n">support</span><span class="o">.</span><span class="n">create_gc_testfile</span><span class="p">,</span>
<a name="cl-53"></a>                                                <span class="n">ROLE_TMPL</span><span class="p">,</span>
<a name="cl-54"></a>                                                <span class="n">textwrap</span><span class="o">.</span><span class="n">dedent</span><span class="p">(</span><span class="s">&quot;&quot;&quot;</span>
<a name="cl-55"></a><span class="s">the_template </span><span class="si">%(whole)s</span><span class="s"></span>
<a name="cl-56"></a><span class="s">&quot;&quot;&quot;</span><span class="p">))</span>
<a name="cl-57"></a>
<a name="cl-58"></a><span class="nd">@with_setup</span><span class="p">(</span><span class="n">tmpl_full_role_creator</span><span class="p">,</span> <span class="n">support</span><span class="o">.</span><span class="n">clean_gc_testfiles</span><span class="p">)</span>
<a name="cl-59"></a><span class="k">def</span> <span class="nf">test_full_role</span><span class="p">():</span>
<a name="cl-60"></a>    <span class="n">fullrole_src</span> <span class="o">=</span> <span class="n">StringIO</span><span class="p">(</span><span class="n">textwrap</span><span class="o">.</span><span class="n">dedent</span><span class="p">(</span><span class="s">&quot;&quot;&quot;</span>
<a name="cl-61"></a><span class="s">    Some text :foo:`Some test text` after</span>
<a name="cl-62"></a><span class="s">    &quot;&quot;&quot;</span><span class="p">))</span>
<a name="cl-63"></a>
<a name="cl-64"></a>    <span class="n">rolesmod</span> <span class="o">=</span> <span class="n">imp</span><span class="o">.</span><span class="n">new_module</span><span class="p">(</span><span class="s">&#39;roles&#39;</span><span class="p">)</span>
<a name="cl-65"></a>    <span class="n">rolesmod</span><span class="o">.</span><span class="n">role_foo</span> <span class="o">=</span> <span class="n">role_foo</span>
<a name="cl-66"></a>    <span class="n">main</span><span class="o">.</span><span class="n">_import</span> <span class="o">=</span> <span class="k">lambda</span> <span class="n">m</span><span class="p">,</span> <span class="n">r</span><span class="p">:</span> <span class="n">rolesmod</span>
<a name="cl-67"></a>    <span class="n">capture</span> <span class="o">=</span> <span class="n">StringIO</span><span class="p">()</span>
<a name="cl-68"></a>    <span class="n">rc</span> <span class="o">=</span> <span class="n">main</span><span class="o">.</span><span class="n">commandline</span><span class="p">([</span><span class="s">&#39;--template=</span><span class="si">%s</span><span class="s">&#39;</span> <span class="o">%</span> <span class="n">ROLE_TMPL</span><span class="p">,</span> <span class="s">&#39;--writer=pseudoxml&#39;</span><span class="p">],</span>
<a name="cl-69"></a>                          <span class="n">source</span><span class="o">=</span><span class="n">fullrole_src</span><span class="p">,</span> <span class="n">destination</span><span class="o">=</span><span class="n">capture</span><span class="p">)</span>
<a name="cl-70"></a>    <span class="n">out</span> <span class="o">=</span> <span class="n">capture</span><span class="o">.</span><span class="n">getvalue</span><span class="p">()</span>
<a name="cl-71"></a>    <span class="n">assert_true</span><span class="p">(</span><span class="s">&#39;ROLESTART_Some test text_ROLESTOP&#39;</span> <span class="ow">in</span> <span class="n">out</span><span class="p">)</span>
<a name="cl-72"></a>
<a name="cl-73"></a><span class="n">SIMPLE_INFILE_PATH</span> <span class="o">=</span> <span class="s">&#39;/tmp/simple_infile.rst&#39;</span>
<a name="cl-74"></a>
<a name="cl-75"></a><span class="n">simple_infile_creator</span> <span class="o">=</span> <span class="n">functools</span><span class="o">.</span><span class="n">partial</span><span class="p">(</span><span class="n">support</span><span class="o">.</span><span class="n">create_gc_testfile</span><span class="p">,</span>
<a name="cl-76"></a>                                          <span class="n">SIMPLE_INFILE_PATH</span><span class="p">,</span>
<a name="cl-77"></a>                                          <span class="n">get_minimal_fixture</span><span class="p">()</span><span class="o">.</span><span class="n">getvalue</span><span class="p">())</span>
<a name="cl-78"></a>
<a name="cl-79"></a><span class="nd">@with_setup</span><span class="p">(</span><span class="n">simple_infile_creator</span><span class="p">,</span> <span class="n">support</span><span class="o">.</span><span class="n">clean_gc_testfiles</span><span class="p">)</span>
<a name="cl-80"></a><span class="k">def</span> <span class="nf">test_w_infile</span><span class="p">():</span>
<a name="cl-81"></a>    <span class="n">capture</span> <span class="o">=</span> <span class="n">StringIO</span><span class="p">()</span>
<a name="cl-82"></a>    <span class="n">rc</span> <span class="o">=</span> <span class="n">main</span><span class="o">.</span><span class="n">commandline</span><span class="p">([</span><span class="s">&#39;--infile=</span><span class="si">%s</span><span class="s">&#39;</span> <span class="o">%</span> <span class="n">SIMPLE_INFILE_PATH</span><span class="p">,</span> <span class="s">&#39;--writer=html&#39;</span><span class="p">],</span>
<a name="cl-83"></a>                          <span class="n">destination</span><span class="o">=</span><span class="n">capture</span><span class="p">)</span>
<a name="cl-84"></a>    <span class="n">assert_equals</span><span class="p">(</span><span class="n">rc</span><span class="p">,</span> <span class="mi">0</span><span class="p">)</span>
<a name="cl-85"></a>    <span class="n">assert_true</span><span class="p">(</span><span class="s">&#39;&lt;title&gt;654321&lt;/title&gt;&#39;</span> <span class="ow">in</span> <span class="n">capture</span><span class="o">.</span><span class="n">getvalue</span><span class="p">())</span>
<a name="cl-86"></a>
<a name="cl-87"></a><span class="n">SIMPLE_OUTFILE</span> <span class="o">=</span> <span class="s">&#39;/tmp/simple_outfile.html&#39;</span>
<a name="cl-88"></a>
<a name="cl-89"></a><span class="nd">@with_setup</span><span class="p">(</span><span class="k">lambda</span><span class="p">:</span> <span class="bp">None</span><span class="p">,</span> <span class="n">functools</span><span class="o">.</span><span class="n">partial</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">unlink</span><span class="p">,</span> <span class="n">SIMPLE_OUTFILE</span><span class="p">))</span>
<a name="cl-90"></a><span class="k">def</span> <span class="nf">test_w_outfile</span><span class="p">():</span>
<a name="cl-91"></a>    <span class="n">rc</span> <span class="o">=</span> <span class="n">main</span><span class="o">.</span><span class="n">commandline</span><span class="p">([</span><span class="s">&#39;--outfile=</span><span class="si">%s</span><span class="s">&#39;</span> <span class="o">%</span> <span class="n">SIMPLE_OUTFILE</span><span class="p">,</span> <span class="s">&#39;--writer=html&#39;</span><span class="p">],</span>
<a name="cl-92"></a>                          <span class="n">source</span><span class="o">=</span><span class="n">get_minimal_fixture</span><span class="p">())</span>
<a name="cl-93"></a>    <span class="n">assert_equals</span><span class="p">(</span><span class="n">rc</span><span class="p">,</span> <span class="mi">0</span><span class="p">)</span>
<a name="cl-94"></a>    <span class="n">assert_true</span><span class="p">(</span><span class="s">&#39;&lt;title&gt;654321&lt;/title&gt;&#39;</span> <span class="ow">in</span> <span class="nb">open</span><span class="p">(</span><span class="n">SIMPLE_OUTFILE</span><span class="p">,</span> <span class="s">&#39;r&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">read</span><span class="p">())</span>
<a name="cl-95"></a>
<a name="cl-96"></a><span class="n">full_latex_dir</span> <span class="o">=</span> <span class="p">[]</span>
<a name="cl-97"></a>
<a name="cl-98"></a><span class="k">def</span> <span class="nf">setup_latex_dir</span><span class="p">():</span>
<a name="cl-99"></a>    <span class="n">full_latex_dir</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">tempfile</span><span class="o">.</span><span class="n">mkdtemp</span><span class="p">(</span><span class="n">prefix</span><span class="o">=</span><span class="s">&#39;fr-latex2pdf-smoketest-&#39;</span><span class="p">))</span>
<a name="cl-100"></a>
<a name="cl-101"></a><span class="k">def</span> <span class="nf">teardown_latex_dir</span><span class="p">():</span>
<a name="cl-102"></a>    <span class="n">shutil</span><span class="o">.</span><span class="n">rmtree</span><span class="p">(</span><span class="n">full_latex_dir</span><span class="p">[</span><span class="mi">0</span><span class="p">])</span>
<a name="cl-103"></a>
<a name="cl-104"></a><span class="k">def</span> <span class="nf">latex_tmp</span><span class="p">(</span><span class="n">name</span><span class="p">):</span>
<a name="cl-105"></a>    <span class="k">return</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">full_latex_dir</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="n">name</span><span class="p">)</span>
<a name="cl-106"></a>
<a name="cl-107"></a><span class="nd">@with_setup</span><span class="p">(</span><span class="n">setup_latex_dir</span><span class="p">,</span> <span class="n">teardown_latex_dir</span><span class="p">)</span>
<a name="cl-108"></a><span class="k">def</span> <span class="nf">test_smoketest_latex2pdf_writing</span><span class="p">():</span>
<a name="cl-109"></a>    <span class="n">rst_path</span> <span class="o">=</span> <span class="n">latex_tmp</span><span class="p">(</span><span class="s">&#39;rst-source.rst&#39;</span><span class="p">)</span>
<a name="cl-110"></a>    <span class="n">support</span><span class="o">.</span><span class="n">write_test_file</span><span class="p">(</span><span class="n">rst_path</span><span class="p">,</span> <span class="n">support</span><span class="o">.</span><span class="n">MINIMAL_FIXTURE</span><span class="p">)</span>
<a name="cl-111"></a>    <span class="n">test_tex</span><span class="o">.</span><span class="n">write_fake_style</span><span class="p">(</span><span class="n">latex_tmp</span><span class="p">(</span><span class="s">&#39;flexifake.sty&#39;</span><span class="p">))</span>
<a name="cl-112"></a>    <span class="c"># XXX: Todo, create a template that demands the style file.</span>
<a name="cl-113"></a>
<a name="cl-114"></a>    <span class="n">capture</span> <span class="o">=</span> <span class="n">StringIO</span><span class="p">()</span>
<a name="cl-115"></a>    <span class="n">rc</span> <span class="o">=</span> <span class="n">main</span><span class="o">.</span><span class="n">commandline</span><span class="p">([</span><span class="s">&#39;--infile=</span><span class="si">%s</span><span class="s">&#39;</span> <span class="o">%</span> <span class="n">rst_path</span><span class="p">,</span> <span class="s">&#39;--writer=latex2pdf&#39;</span><span class="p">],</span>
<a name="cl-116"></a>                          <span class="n">destination</span><span class="o">=</span><span class="n">capture</span><span class="p">)</span>
<a name="cl-117"></a>    <span class="n">assert_equals</span><span class="p">(</span><span class="n">rc</span><span class="p">,</span> <span class="mi">0</span><span class="p">)</span>
<a name="cl-118"></a>    <span class="n">pdf</span> <span class="o">=</span> <span class="n">capture</span><span class="o">.</span><span class="n">getvalue</span><span class="p">()</span>
<a name="cl-119"></a>    <span class="n">assert_equals</span><span class="p">(</span><span class="n">pdf</span><span class="p">[:</span><span class="mi">8</span><span class="p">],</span> <span class="s">&#39;%PDF-1.4&#39;</span><span class="p">)</span>
<a name="cl-120"></a>    <span class="n">assert_equals</span><span class="p">(</span><span class="n">pdf</span><span class="p">[</span><span class="o">-</span><span class="mi">6</span><span class="p">:],</span> <span class="s">&#39;</span><span class="si">%%</span><span class="s">EOF</span><span class="se">\n</span><span class="s">&#39;</span><span class="p">)</span>
</pre></div>
</td></tr></table>
		
	
</div>



			<div class="cb"></div>
		</div>
		<div class="cb footer-placeholder"></div>
	</div>
	<div id="footer-wrapper">
		<div id="footer">
			<a href="/site/terms/">TOS</a> | <a href="/site/privacy/">Privacy Policy</a> | <a href="http://blog.bitbucket.org/">Blog</a> | <a href="http://bitbucket.org/jespern/bitbucket/issues/new/">Report Bug</a> | <a href="http://groups.google.com/group/bitbucket-users">Discuss</a> | <a href="http://avantlumiere.com/">&copy; 2008-2009</a>
			| We run <small><b>
				<a href="http://www.djangoproject.com/">Django 1.1.0</a> / 
				<a href="http://bitbucket.org/jespern/django-piston/">Piston 0.2.3rc1</a> / 
				<a href="http://www.selenic.com/mercurial/">Hg 1.3.1</a> / 
				<a href="http://www.python.org">Python 2.5.2</a> /
				r2710
			</b></small>
		</div>
	</div>
	<script type="text/javascript">
	var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
	document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
	</script>
	<script type="text/javascript">
	var pt = _gat._getTracker("UA-2456069-3");
	pt._trackPageview();
	</script>
</body>
</html>
