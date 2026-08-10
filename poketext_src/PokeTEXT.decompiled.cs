using System;
using System.CodeDom.Compiler;
using System.Collections;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.ComponentModel.Design;
using System.Configuration;
using System.Diagnostics;
using System.Drawing;
using System.Globalization;
using System.IO;
using System.Reflection;
using System.Resources;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using System.Runtime.Versioning;
using System.Threading;
using System.Windows.Forms;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.ApplicationServices;
using Microsoft.VisualBasic.CompilerServices;
using Microsoft.VisualBasic.Devices;
using Microsoft.VisualBasic.FileIO;
using PokeTEXT.My;

[assembly: CompilationRelaxations(8)]
[assembly: RuntimeCompatibility(WrapNonExceptionThrows = true)]
[assembly: Debuggable(DebuggableAttribute.DebuggingModes.Default | DebuggableAttribute.DebuggingModes.DisableOptimizations | DebuggableAttribute.DebuggingModes.IgnoreSymbolStoreSequencePoints | DebuggableAttribute.DebuggingModes.EnableEditAndContinue)]
[assembly: AssemblyTitle("PokeTEXT")]
[assembly: AssemblyDescription("パワポケ文字コード変換ツール")]
[assembly: AssemblyCompany("")]
[assembly: AssemblyProduct("PokeTEXT")]
[assembly: AssemblyCopyright("Copyright ©  2020-2025 インデゴ")]
[assembly: AssemblyTrademark("")]
[assembly: ComVisible(false)]
[assembly: Guid("29b66d6e-6ec6-4c86-8fa6-cec544ab05d5")]
[assembly: AssemblyFileVersion("1.1.2.1")]
[assembly: TargetFramework(".NETFramework,Version=v4.8", FrameworkDisplayName = ".NET Framework 4.8")]
[assembly: AssemblyVersion("1.1.2.1")]
namespace PokeTEXT.My
{
	[GeneratedCode("MyTemplate", "11.0.0.0")]
	[EditorBrowsable(EditorBrowsableState.Never)]
	internal class MyApplication : WindowsFormsApplicationBase
	{
		[MethodImpl(MethodImplOptions.NoInlining | MethodImplOptions.NoOptimization)]
		[STAThread]
		[DebuggerHidden]
		[EditorBrowsable(EditorBrowsableState.Advanced)]
		internal static void Main(string[] Args)
		{
			try
			{
				Application.SetCompatibleTextRenderingDefault(WindowsFormsApplicationBase.UseCompatibleTextRendering);
			}
			finally
			{
			}
			MyProject.Application.Run(Args);
		}

		[DebuggerStepThrough]
		public MyApplication()
			: base(AuthenticationMode.Windows)
		{
			base.IsSingleInstance = false;
			base.EnableVisualStyles = true;
			base.SaveMySettingsOnExit = false;
			base.ShutdownStyle = ShutdownMode.AfterMainFormCloses;
		}

		[DebuggerStepThrough]
		protected override void OnCreateMainForm()
		{
			base.MainForm = MyProject.Forms.PokeTEXT_Form;
		}

		[DebuggerStepThrough]
		protected override bool OnInitialize(ReadOnlyCollection<string> commandLineArgs)
		{
			base.MinimumSplashScreenDisplayTime = 0;
			return base.OnInitialize(commandLineArgs);
		}
	}
	[GeneratedCode("MyTemplate", "11.0.0.0")]
	[EditorBrowsable(EditorBrowsableState.Never)]
	internal class MyComputer : Computer
	{
		[DebuggerHidden]
		[EditorBrowsable(EditorBrowsableState.Never)]
		public MyComputer()
		{
		}
	}
	[StandardModule]
	[HideModuleName]
	[GeneratedCode("MyTemplate", "11.0.0.0")]
	internal sealed class MyProject
	{
		[EditorBrowsable(EditorBrowsableState.Never)]
		[MyGroupCollection("System.Windows.Forms.Form", "Create__Instance__", "Dispose__Instance__", "My.MyProject.Forms")]
		internal sealed class MyForms
		{
			[ThreadStatic]
			private static Hashtable m_FormBeingCreated;

			[EditorBrowsable(EditorBrowsableState.Never)]
			public PokeTEXT_Form m_PokeTEXT_Form;

			public PokeTEXT_Form PokeTEXT_Form
			{
				[DebuggerHidden]
				get
				{
					m_PokeTEXT_Form = Create__Instance__(m_PokeTEXT_Form);
					return m_PokeTEXT_Form;
				}
				[DebuggerHidden]
				set
				{
					if (value != m_PokeTEXT_Form)
					{
						if (value != null)
						{
							throw new ArgumentException("Property can only be set to Nothing");
						}
						Dispose__Instance__(ref m_PokeTEXT_Form);
					}
				}
			}

			[DebuggerHidden]
			private static T Create__Instance__<T>(T Instance) where T : Form, new()
			{
				if (Instance == null || Instance.IsDisposed)
				{
					if (m_FormBeingCreated != null)
					{
						if (m_FormBeingCreated.ContainsKey(typeof(T)))
						{
							throw new InvalidOperationException(Utils.GetResourceString("WinForms_RecursiveFormCreate"));
						}
					}
					else
					{
						m_FormBeingCreated = new Hashtable();
					}
					m_FormBeingCreated.Add(typeof(T), null);
					try
					{
						return new T();
					}
					catch (TargetInvocationException ex) when (((Func<bool>)delegate
					{
						// Could not convert BlockContainer to single expression
						ProjectData.SetProjectError(ex);
						return ex.InnerException != null;
					}).Invoke())
					{
						string resourceString = Utils.GetResourceString("WinForms_SeeInnerException", ex.InnerException.Message);
						throw new InvalidOperationException(resourceString, ex.InnerException);
					}
					finally
					{
						m_FormBeingCreated.Remove(typeof(T));
					}
				}
				return Instance;
			}

			[DebuggerHidden]
			private void Dispose__Instance__<T>(ref T instance) where T : Form
			{
				instance.Dispose();
				instance = null;
			}

			[DebuggerHidden]
			[EditorBrowsable(EditorBrowsableState.Never)]
			public MyForms()
			{
			}

			[EditorBrowsable(EditorBrowsableState.Never)]
			public override bool Equals(object o)
			{
				return base.Equals(RuntimeHelpers.GetObjectValue(o));
			}

			[EditorBrowsable(EditorBrowsableState.Never)]
			public override int GetHashCode()
			{
				return base.GetHashCode();
			}

			[EditorBrowsable(EditorBrowsableState.Never)]
			internal new Type GetType()
			{
				return typeof(MyForms);
			}

			[EditorBrowsable(EditorBrowsableState.Never)]
			public override string ToString()
			{
				return base.ToString();
			}
		}

		[EditorBrowsable(EditorBrowsableState.Never)]
		[MyGroupCollection("System.Web.Services.Protocols.SoapHttpClientProtocol", "Create__Instance__", "Dispose__Instance__", "")]
		internal sealed class MyWebServices
		{
			[EditorBrowsable(EditorBrowsableState.Never)]
			[DebuggerHidden]
			public override bool Equals(object o)
			{
				return base.Equals(RuntimeHelpers.GetObjectValue(o));
			}

			[EditorBrowsable(EditorBrowsableState.Never)]
			[DebuggerHidden]
			public override int GetHashCode()
			{
				return base.GetHashCode();
			}

			[EditorBrowsable(EditorBrowsableState.Never)]
			[DebuggerHidden]
			internal new Type GetType()
			{
				return typeof(MyWebServices);
			}

			[EditorBrowsable(EditorBrowsableState.Never)]
			[DebuggerHidden]
			public override string ToString()
			{
				return base.ToString();
			}

			[DebuggerHidden]
			private static T Create__Instance__<T>(T instance) where T : new()
			{
				if (instance == null)
				{
					return new T();
				}
				return instance;
			}

			[DebuggerHidden]
			private void Dispose__Instance__<T>(ref T instance)
			{
				instance = default(T);
			}

			[DebuggerHidden]
			[EditorBrowsable(EditorBrowsableState.Never)]
			public MyWebServices()
			{
			}
		}

		[EditorBrowsable(EditorBrowsableState.Never)]
		[ComVisible(false)]
		internal sealed class ThreadSafeObjectProvider<T> where T : new()
		{
			[CompilerGenerated]
			[ThreadStatic]
			private static T m_ThreadStaticValue;

			internal T GetInstance
			{
				[DebuggerHidden]
				get
				{
					if (m_ThreadStaticValue == null)
					{
						m_ThreadStaticValue = new T();
					}
					return m_ThreadStaticValue;
				}
			}

			[DebuggerHidden]
			[EditorBrowsable(EditorBrowsableState.Never)]
			public ThreadSafeObjectProvider()
			{
			}
		}

		private static readonly ThreadSafeObjectProvider<MyComputer> m_ComputerObjectProvider = new ThreadSafeObjectProvider<MyComputer>();

		private static readonly ThreadSafeObjectProvider<MyApplication> m_AppObjectProvider = new ThreadSafeObjectProvider<MyApplication>();

		private static readonly ThreadSafeObjectProvider<User> m_UserObjectProvider = new ThreadSafeObjectProvider<User>();

		private static ThreadSafeObjectProvider<MyForms> m_MyFormsObjectProvider = new ThreadSafeObjectProvider<MyForms>();

		private static readonly ThreadSafeObjectProvider<MyWebServices> m_MyWebServicesObjectProvider = new ThreadSafeObjectProvider<MyWebServices>();

		[HelpKeyword("My.Computer")]
		internal static MyComputer Computer
		{
			[DebuggerHidden]
			get
			{
				return m_ComputerObjectProvider.GetInstance;
			}
		}

		[HelpKeyword("My.Application")]
		internal static MyApplication Application
		{
			[DebuggerHidden]
			get
			{
				return m_AppObjectProvider.GetInstance;
			}
		}

		[HelpKeyword("My.User")]
		internal static User User
		{
			[DebuggerHidden]
			get
			{
				return m_UserObjectProvider.GetInstance;
			}
		}

		[HelpKeyword("My.Forms")]
		internal static MyForms Forms
		{
			[DebuggerHidden]
			get
			{
				return m_MyFormsObjectProvider.GetInstance;
			}
		}

		[HelpKeyword("My.WebServices")]
		internal static MyWebServices WebServices
		{
			[DebuggerHidden]
			get
			{
				return m_MyWebServicesObjectProvider.GetInstance;
			}
		}
	}
}
namespace PokeTEXT.My.Resources
{
	[StandardModule]
	[GeneratedCode("System.Resources.Tools.StronglyTypedResourceBuilder", "17.0.0.0")]
	[DebuggerNonUserCode]
	[CompilerGenerated]
	[HideModuleName]
	internal sealed class Resources
	{
		private static ResourceManager resourceMan;

		private static CultureInfo resourceCulture;

		[EditorBrowsable(EditorBrowsableState.Advanced)]
		internal static ResourceManager ResourceManager
		{
			get
			{
				if (object.ReferenceEquals(resourceMan, null))
				{
					ResourceManager resourceManager = new ResourceManager("PokeTEXT.Resources", typeof(Resources).Assembly);
					resourceMan = resourceManager;
				}
				return resourceMan;
			}
		}

		[EditorBrowsable(EditorBrowsableState.Advanced)]
		internal static CultureInfo Culture
		{
			get
			{
				return resourceCulture;
			}
			set
			{
				resourceCulture = value;
			}
		}
	}
}
namespace PokeTEXT.My
{
	[CompilerGenerated]
	[GeneratedCode("Microsoft.VisualStudio.Editors.SettingsDesigner.SettingsSingleFileGenerator", "17.10.0.0")]
	[EditorBrowsable(EditorBrowsableState.Advanced)]
	internal sealed class MySettings : ApplicationSettingsBase
	{
		private static MySettings defaultInstance = (MySettings)SettingsBase.Synchronized(new MySettings());

		private static bool addedHandler;

		private static object addedHandlerLockObject = RuntimeHelpers.GetObjectValue(new object());

		public static MySettings Default
		{
			get
			{
				if (!addedHandler)
				{
					object obj = addedHandlerLockObject;
					ObjectFlowControl.CheckForSyncLockOnValueType(obj);
					bool lockTaken = false;
					try
					{
						Monitor.Enter(obj, ref lockTaken);
						if (!addedHandler)
						{
							MyProject.Application.Shutdown += [DebuggerNonUserCode] [EditorBrowsable(EditorBrowsableState.Advanced)] (object sender, EventArgs e) =>
							{
								if (MyProject.Application.SaveMySettingsOnExit)
								{
									MySettingsProperty.Settings.Save();
								}
							};
							addedHandler = true;
						}
					}
					finally
					{
						if (lockTaken)
						{
							Monitor.Exit(obj);
						}
					}
				}
				return defaultInstance;
			}
		}

		[DebuggerNonUserCode]
		[EditorBrowsable(EditorBrowsableState.Advanced)]
		private static void AutoSaveSettings(object sender, EventArgs e)
		{
			if (MyProject.Application.SaveMySettingsOnExit)
			{
				MySettingsProperty.Settings.Save();
			}
		}
	}
	[StandardModule]
	[HideModuleName]
	[DebuggerNonUserCode]
	[CompilerGenerated]
	internal sealed class MySettingsProperty
	{
		[HelpKeyword("My.Settings")]
		internal static MySettings Settings => MySettings.Default;
	}
}
namespace PokeTEXT
{
	[DesignerGenerated]
	public class PokeTEXT_Form : Form
	{
		private IContainer components;

		[CompilerGenerated]
		[DebuggerBrowsable(DebuggerBrowsableState.Never)]
		[AccessedThroughProperty("参照")]
		private Button _参照;

		[CompilerGenerated]
		[DebuggerBrowsable(DebuggerBrowsableState.Never)]
		[AccessedThroughProperty("ファイル選択")]
		private OpenFileDialog _ファイル選択;

		[CompilerGenerated]
		[DebuggerBrowsable(DebuggerBrowsableState.Never)]
		[AccessedThroughProperty("実行")]
		private CheckBox _実行;

		internal virtual Button 参照
		{
			[CompilerGenerated]
			get
			{
				return _参照;
			}
			[MethodImpl(MethodImplOptions.Synchronized)]
			[CompilerGenerated]
			set
			{
				EventHandler value2 = 参照_Click;
				Button button = _参照;
				if (button != null)
				{
					button.Click -= value2;
				}
				_参照 = value;
				button = _参照;
				if (button != null)
				{
					button.Click += value2;
				}
			}
		}

		[field: AccessedThroughProperty("処理進行状況")]
		internal virtual ProgressBar 処理進行状況
		{
			get; [MethodImpl(MethodImplOptions.Synchronized)]
			set;
		}

		[field: AccessedThroughProperty("参照ファイル名表示")]
		internal virtual TextBox 参照ファイル名表示
		{
			get; [MethodImpl(MethodImplOptions.Synchronized)]
			set;
		}

		internal virtual OpenFileDialog ファイル選択
		{
			[CompilerGenerated]
			get
			{
				return _ファイル選択;
			}
			[MethodImpl(MethodImplOptions.Synchronized)]
			[CompilerGenerated]
			set
			{
				CancelEventHandler value2 = ファイル選択_FileOk;
				OpenFileDialog openFileDialog = _ファイル選択;
				if (openFileDialog != null)
				{
					openFileDialog.FileOk -= value2;
				}
				_ファイル選択 = value;
				openFileDialog = _ファイル選択;
				if (openFileDialog != null)
				{
					openFileDialog.FileOk += value2;
				}
			}
		}

		[field: AccessedThroughProperty("参照ファイルLabel")]
		internal virtual Label 参照ファイルLabel
		{
			get; [MethodImpl(MethodImplOptions.Synchronized)]
			set;
		}

		[field: AccessedThroughProperty("経過表示Label")]
		internal virtual Label 経過表示Label
		{
			get; [MethodImpl(MethodImplOptions.Synchronized)]
			set;
		}

		internal virtual CheckBox 実行
		{
			[CompilerGenerated]
			get
			{
				return _実行;
			}
			[MethodImpl(MethodImplOptions.Synchronized)]
			[CompilerGenerated]
			set
			{
				EventHandler value2 = 実行_CheckedChanged;
				CheckBox checkBox = _実行;
				if (checkBox != null)
				{
					checkBox.CheckedChanged -= value2;
				}
				_実行 = value;
				checkBox = _実行;
				if (checkBox != null)
				{
					checkBox.CheckedChanged += value2;
				}
			}
		}

		[field: AccessedThroughProperty("文字コード選択ComboBox")]
		internal virtual ComboBox 文字コード選択ComboBox
		{
			get; [MethodImpl(MethodImplOptions.Synchronized)]
			set;
		}

		[field: AccessedThroughProperty("文字コード選択Label")]
		internal virtual Label 文字コード選択Label
		{
			get; [MethodImpl(MethodImplOptions.Synchronized)]
			set;
		}

		[field: AccessedThroughProperty("アドレスありCheckBox")]
		internal virtual CheckBox アドレスありCheckBox
		{
			get; [MethodImpl(MethodImplOptions.Synchronized)]
			set;
		}

		[field: AccessedThroughProperty("十六進データありCheckBox")]
		internal virtual CheckBox 十六進データありCheckBox
		{
			get; [MethodImpl(MethodImplOptions.Synchronized)]
			set;
		}

		[field: AccessedThroughProperty("出力オプションGroupBox")]
		internal virtual GroupBox 出力オプションGroupBox
		{
			get; [MethodImpl(MethodImplOptions.Synchronized)]
			set;
		}

		[field: AccessedThroughProperty("蓄積データ出力NumericUpDown")]
		internal virtual NumericUpDown 蓄積データ出力NumericUpDown
		{
			get; [MethodImpl(MethodImplOptions.Synchronized)]
			set;
		}

		[field: AccessedThroughProperty("蓄積データ出力Label")]
		internal virtual Label 蓄積データ出力Label
		{
			get; [MethodImpl(MethodImplOptions.Synchronized)]
			set;
		}

		[field: AccessedThroughProperty("Wait間隔NumericUpDown")]
		internal virtual NumericUpDown Wait間隔NumericUpDown
		{
			get; [MethodImpl(MethodImplOptions.Synchronized)]
			set;
		}

		[field: AccessedThroughProperty("補足")]
		internal virtual ToolTip 補足
		{
			get; [MethodImpl(MethodImplOptions.Synchronized)]
			set;
		}

		[field: AccessedThroughProperty("Wait間隔Label")]
		internal virtual Label Wait間隔Label
		{
			get; [MethodImpl(MethodImplOptions.Synchronized)]
			set;
		}

		[field: AccessedThroughProperty("Wait時間NumericUpDown")]
		internal virtual NumericUpDown Wait時間NumericUpDown
		{
			get; [MethodImpl(MethodImplOptions.Synchronized)]
			set;
		}

		[field: AccessedThroughProperty("Wait時間Label")]
		internal virtual Label Wait時間Label
		{
			get; [MethodImpl(MethodImplOptions.Synchronized)]
			set;
		}

		[field: AccessedThroughProperty("アドレス化表示CheckBox")]
		internal virtual CheckBox アドレス化表示CheckBox
		{
			get; [MethodImpl(MethodImplOptions.Synchronized)]
			set;
		}

		public PokeTEXT_Form()
		{
			base.FormClosing += PokeTEXT_Form_FormClosing;
			base.Load += PokeTEXT_Form_Load;
			InitializeComponent();
		}

		public ulong GetLinesOfTextFile(string FileName)
		{
			StreamReader streamReader = new StreamReader(FileName);
			checked
			{
				int num = default(int);
				while (streamReader.Peek() >= 0)
				{
					streamReader.ReadLine();
					num++;
				}
				return (ulong)num;
			}
		}

		private void 参照_Click(object sender, EventArgs e)
		{
			ファイル選択.ShowDialog();
		}

		private void 実行_CheckedChanged(object sender, EventArgs e)
		{
			if (Operators.CompareString(参照ファイル名表示.Text, "", TextCompare: false) == 0)
			{
				MessageBox.Show(this, "ファイルの参照先を指定してください。", "参照ファイルエラー", MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
				return;
			}
			if (文字コード選択ComboBox.SelectedIndex == -1)
			{
				文字コード選択ComboBox.SelectedIndex = 15;
			}
			if (Operators.CompareString(実行.Text, "実行", TextCompare: false) == 0)
			{
				実行.Text = "中止";
				Application.DoEvents();
				int selectedIndex = 文字コード選択ComboBox.SelectedIndex;
				if (selectedIndex == 0 || selectedIndex == 1)
				{
					ポケ1と2の文字コード変換処理();
				}
				else if (selectedIndex >= 2 && selectedIndex <= 17)
				{
					ポケ3以降の文字コード変換処理();
				}
			}
			if (Operators.CompareString(実行.Text, "中止", TextCompare: false) == 0)
			{
				実行.Text = "実行";
				Application.DoEvents();
			}
		}

		public void ポケ1と2の文字コード変換処理()
		{
			checked
			{
				if (MyProject.Computer.FileSystem.FileExists(参照ファイル名表示.Text))
				{
					出力オプションGroupBox.Enabled = false;
					文字コード選択ComboBox.Enabled = false;
					参照ファイル名表示.Enabled = false;
					参照.Enabled = false;
					using TextFieldParser textFieldParser = new TextFieldParser(参照ファイル名表示.Text);
					ulong[] array = new ulong[51];
					long[] array2 = new long[5];
					byte[] array3 = new byte[17];
					string[] array4 = new string[3];
					byte b = 0;
					if (アドレスありCheckBox.Checked)
					{
						b++;
					}
					if (十六進データありCheckBox.Checked)
					{
						b += 2;
					}
					if (アドレス化表示CheckBox.Checked)
					{
						b += 4;
					}
					ulong num = Convert.ToUInt64(Wait時間NumericUpDown.Value);
					array4[1] = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉっゃゅょがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンァィゥェォッャュョガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポヴＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ０１２３４５６７８９！？・ー❤ｒ％○×「」／吉▼▼→負員凶⇒（）塁投保ー二三遊左中右外野球手広角打法流守両高校巧速筋技対内。、－＋\u3000\u3000\u3000";
					switch (文字コード選択ComboBox.SelectedIndex)
					{
					case 0:
						array4[2] = "安気練習部血殺死室団自分試合人入下上男女出見大会学校言海走今日明★体～学園話以電変化恋能月回先生勝年\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000";
						break;
					case 1:
						array4[2] = "安気練習部血殺死室団自分試合人入下上男女出見大会学校言海走今日明★体～学園話以電変化恋能月回先生勝年社長位俸億万金円来酒軍利率狂低発子心実世多少知書文秘者早行場目私店間何休当評価良仲返事考身小食水火好他全前名帰思王楽方戻別土伍曹山空客首正元争千古新高駅公時士本兄供株式況氏斗寮仕春夏秋冬♪戦神様不彼天同訓練四代根性国赤字■界病呪凡伝自超伝説選送盗失敗初振番強弱花症短定悪運反応直寸仙呼向付肩術点席使備逆逃虫歯治信昨車重君形決足用数合牛丼止亡買払貯怪獣佐作魚丈夫件告汗句油東西南北動司令隊主再販売第弾放色父\u3000き入Ｔ";
						break;
					}
					ulong num2 = 0uL;
					ulong value = 0uL;
					ulong value2 = 1uL;
					ulong num3 = 1uL;
					ulong value3 = 0uL;
					ulong num4 = 1uL;
					ulong num5 = 1uL;
					処理進行状況.Value = 0;
					ulong num6 = Convert.ToUInt64(decimal.Subtract(new decimal(GetLinesOfTextFile(参照ファイル名表示.Text)), 2m));
					ulong num7 = 1uL;
					string str = "";
					string text = "";
					byte b2 = 0;
					byte b3 = 0;
					byte b4 = 0;
					ulong value4 = 0uL;
					byte b5 = 0;
					textFieldParser.TextFieldType = FieldType.Delimited;
					textFieldParser.SetDelimiters("区切りなし");
					ulong num8 = default(ulong);
					while (!textFieldParser.EndOfData)
					{
						string[] array5 = textFieldParser.ReadFields();
						string[] array6 = array5;
						foreach (string text2 in array6)
						{
							string text3 = text2;
							if (decimal.Compare(new decimal(value2), 3m) >= 0)
							{
								if (Operators.CompareString(Strings.Mid(text3, 11, 2), "  ", TextCompare: false) != 0)
								{
									array3[1] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 11, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 14, 2), "  ", TextCompare: false) != 0)
								{
									array3[2] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 14, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 17, 2), "  ", TextCompare: false) != 0)
								{
									array3[3] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 17, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 20, 2), "  ", TextCompare: false) != 0)
								{
									array3[4] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 20, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 23, 2), "  ", TextCompare: false) != 0)
								{
									array3[5] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 23, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 26, 2), "  ", TextCompare: false) != 0)
								{
									array3[6] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 26, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 29, 2), "  ", TextCompare: false) != 0)
								{
									array3[7] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 29, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 32, 2), "  ", TextCompare: false) != 0)
								{
									array3[8] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 32, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 35, 2), "  ", TextCompare: false) != 0)
								{
									array3[9] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 35, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 38, 2), "  ", TextCompare: false) != 0)
								{
									array3[10] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 38, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 41, 2), "  ", TextCompare: false) != 0)
								{
									array3[11] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 41, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 44, 2), "  ", TextCompare: false) != 0)
								{
									array3[12] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 44, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 47, 2), "  ", TextCompare: false) != 0)
								{
									array3[13] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 47, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 50, 2), "  ", TextCompare: false) != 0)
								{
									array3[14] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 50, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 53, 2), "  ", TextCompare: false) != 0)
								{
									array3[15] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 53, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 56, 2), "  ", TextCompare: false) != 0)
								{
									array3[16] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 56, 2));
								}
								num8 = 0uL;
								num2 = 1uL;
								do
								{
									num8 += array3[(int)num2];
									Application.DoEvents();
									num2++;
								}
								while (num2 <= 16);
								str = text3;
								text3 = "";
								value = 0uL;
								if (アドレスありCheckBox.Checked)
								{
									text3 += Strings.Mid(str, 1, 10);
									value = Convert.ToUInt64(decimal.Add(new decimal(value), 10m));
								}
								if (十六進データありCheckBox.Checked)
								{
									text3 = text3 + Strings.Mid(str, 11, 47) + "  ";
									value = Convert.ToUInt64(decimal.Add(new decimal(value), 49m));
								}
								b3 = (byte)(b2 + 16);
								b4 = b2;
								num2 = 1uL;
								do
								{
									array[(int)(num2 + b2)] = array3[(int)num2];
									num2++;
								}
								while (num2 <= 16);
								ulong num9 = b3;
								for (num2 = 1uL; num2 <= num9; num2++)
								{
									ulong num10 = array[(int)num2];
									if (num10 == 0)
									{
										text3 += " ";
										b2 = 0;
										b5 = 1;
										continue;
									}
									if (num10 >= 1 && num10 <= 252)
									{
										text3 += Strings.Mid(array4[1], (int)array[(int)num2], 1);
										b2 = 0;
										b5 = 1;
										continue;
									}
									switch (num10)
									{
									case 253uL:
									{
										byte b6 = 2;
										if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
										{
											decimal d2 = decimal.Add(decimal.Multiply(new decimal(array[(int)num2]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))]));
											if (decimal.Compare(d2, 64768m) >= 0 && decimal.Compare(d2, 65023m) <= 0)
											{
												text3 += Strings.Mid(array4[2], Convert.ToInt32(decimal.Add(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))]), 1m)), 1);
											}
											b2 = 0;
											b5 = 1;
											num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
										}
										else
										{
											ulong num91 = num2;
											if (num91 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
										}
										break;
									}
									case 254uL:
									{
										unchecked
										{
											if (decimal.Compare(new decimal(value4), 1m) >= 0)
											{
												if (decimal.Compare(new decimal(value4), 1m) == 0)
												{
													if (b5 == 1 && b == 0)
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[選択肢端]";
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													if (b5 == 1 && b == 0)
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[択端]";
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												value4 = Convert.ToUInt64(decimal.Subtract(new decimal(value4), 1m));
												b2 = 0;
												break;
											}
										}
										decimal d = decimal.Add(decimal.Multiply(new decimal(array[(int)num2]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))]));
										byte b6;
										if (decimal.Compare(d, 65024m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												text3 += "[改行]";
												b2 = 0;
												b5 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num11 = num2;
												if (num11 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65025m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												text3 += "▼";
												b2 = 0;
												b5 = 1;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												break;
											}
											ulong num12 = num2;
											if (num12 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											break;
										}
										if (decimal.Compare(d, 65026m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												text3 += "▼[改行]";
												b2 = 0;
												b5 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num13 = num2;
												if (num13 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65027m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												text3 += "▼[消去]";
												b2 = 0;
												b5 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num14 = num2;
												if (num14 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65028m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												text3 += "【名前】";
												b2 = 0;
												b5 = 1;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												break;
											}
											ulong num15 = num2;
											if (num15 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											break;
										}
										if (decimal.Compare(d, 65033m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "[FE09]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num16 = num2;
												if (num16 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65034m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "[FE0A]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num17 = num2;
												if (num17 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65035m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "[FE0B]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num18 = num2;
												if (num18 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65036m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "[文遅]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num19 = num2;
												if (num19 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65037m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "[文戻]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num20 = num2;
												if (num20 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65040m) == 0)
										{
											b6 = 3;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												text3 = text3 + "[音0x" + $"{array2[1]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num21 = num2;
												if (num21 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num21 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65041m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												text3 += "[太字]【";
												b2 = 0;
												b5 = 1;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												break;
											}
											ulong num22 = num2;
											if (num22 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											break;
										}
										if (decimal.Compare(d, 65042m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												text3 += "】";
												b2 = 0;
												b5 = 1;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												break;
											}
											ulong num23 = num2;
											if (num23 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											break;
										}
										if (decimal.Compare(d, 65043m) == 0)
										{
											b6 = 4;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												text3 = text3 + "[数値表示,アドレス0x" + $"{array2[1]:X4}" + "]";
												b2 = 0;
												b5 = 1;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
												break;
											}
											ulong num24 = num2;
											if (num24 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num24 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num24 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											break;
										}
										if (decimal.Compare(d, 65044m) == 0)
										{
											b6 = 3;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												text3 = text3 + "[中絵0x" + $"{array2[1]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num25 = num2;
												if (num25 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num25 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65045m) == 0)
										{
											b6 = 3;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												text3 = text3 + "[左絵0x" + $"{array2[1]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num26 = num2;
												if (num26 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num26 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65046m) == 0)
										{
											b6 = 3;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												text3 = text3 + "[右絵0x" + $"{array2[1]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num27 = num2;
												if (num27 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num27 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65047m) == 0)
										{
											b6 = 5;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												text3 = text3 + "[FE17,アドレス0x" + $"{array2[1]:X4}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num28 = num2;
											if (num28 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num28 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num28 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num28 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											break;
										}
										if (decimal.Compare(d, 65048m) == 0)
										{
											b6 = 5;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												text3 = text3 + "[FE18,アドレス0x" + $"{array2[1]:X4}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num29 = num2;
											if (num29 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num29 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num29 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num29 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											break;
										}
										if (decimal.Compare(d, 65049m) == 0)
										{
											b6 = 5;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												text3 = text3 + "[FE19,アドレス0x" + $"{array2[1]:X4}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num30 = num2;
											if (num30 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num30 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num30 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num30 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											break;
										}
										if (decimal.Compare(d, 65050m) == 0)
										{
											b6 = 3;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 = ((decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 1m) != 0) ? (text3 + "[選択肢1," + Conversions.ToString(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]) + "択]") : (text3 + "[選択肢1,Yes/No]"));
												value4 = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												if (decimal.Compare(new decimal(value4), 2m) < 0)
												{
													value4 = 2uL;
												}
												value4 = Convert.ToUInt64(decimal.Add(new decimal(value4), 1m));
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num31 = num2;
												if (num31 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num31 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65051m) == 0)
										{
											b6 = 3;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 = ((decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 1m) != 0) ? (text3 + "[選択肢2," + Conversions.ToString(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]) + "択]") : (text3 + "[選択肢2,Yes/No]"));
												value4 = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												if (decimal.Compare(new decimal(value4), 2m) < 0)
												{
													value4 = 2uL;
												}
												value4 = Convert.ToUInt64(decimal.Add(new decimal(value4), 1m));
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num32 = num2;
												if (num32 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num32 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65052m) == 0)
										{
											b6 = 4;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												text3 = text3 + "[Case分岐,アドレス0x" + $"{array2[1]:X4}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num33 = num2;
											if (num33 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num33 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num33 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											break;
										}
										if (decimal.Compare(d, 65053m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "[Case0]【";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num34 = num2;
												if (num34 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65054m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "[Case1]【";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num35 = num2;
												if (num35 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65055m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "[Case2]【";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num36 = num2;
												if (num36 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65056m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "[Case3]【";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num37 = num2;
												if (num37 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65057m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "[Case4]【";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num38 = num2;
												if (num38 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65058m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "[Case5]【";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num39 = num2;
												if (num39 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65059m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "[Case6]【";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num40 = num2;
												if (num40 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65060m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "[Case7]【";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num41 = num2;
												if (num41 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65061m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "】";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num42 = num2;
												if (num42 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65062m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "[Case分岐終了]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num43 = num2;
												if (num43 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65063m) == 0)
										{
											b6 = 5;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												text3 = text3 + "[If分岐,アドレス0x" + $"{array2[1]:X4}" + ",0x" + Conversions.ToString(array2[2]) + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num44 = num2;
											if (num44 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num44 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num44 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num44 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											break;
										}
										if (decimal.Compare(d, 65064m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "[Else]【";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num45 = num2;
												if (num45 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65065m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "】";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num46 = num2;
												if (num46 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65067m) == 0)
										{
											b6 = 4;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												text3 = text3 + "[FE2B,アドレス0x" + $"{array2[1]:X4}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num47 = num2;
											if (num47 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num47 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num47 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											break;
										}
										if (decimal.Compare(d, 65068m) == 0)
										{
											b6 = 5;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												text3 = text3 + "[イベ呼出分岐,アドレス0x" + $"{array2[1]:X4}" + ",以後" + Conversions.ToString(array2[2] + 1) + "バイト先まで分岐先アドレス]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num48 = num2;
											if (num48 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num48 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num48 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num48 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											break;
										}
										if (decimal.Compare(d, 65069m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												text3 += "【ポジション】";
												b2 = 0;
												b5 = 1;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												break;
											}
											ulong num49 = num2;
											if (num49 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											break;
										}
										if (decimal.Compare(d, 65070m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												text3 += "【彼女名】";
												b2 = 0;
												b5 = 1;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												break;
											}
											ulong num50 = num2;
											if (num50 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											break;
										}
										if (decimal.Compare(d, 65071m) == 0)
										{
											b6 = 4;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												text3 = text3 + "[FE2F,アドレス0x" + $"{array2[1]:X4}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num51 = num2;
											if (num51 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num51 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num51 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											break;
										}
										if (decimal.Compare(d, 65072m) == 0)
										{
											b6 = 5;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												text3 = text3 + "[FE30,アドレス0x" + $"{array2[1]:X4}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num52 = num2;
											if (num52 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num52 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num52 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num52 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											break;
										}
										if (decimal.Compare(d, 65073m) == 0)
										{
											b6 = 6;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))])));
												text3 = text3 + "[FE31,アドレス0x" + $"{array2[1]:X4}" + ",アドレス0x" + $"{array2[2]:X4}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num53 = num2;
											if (num53 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num53 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num53 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num53 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											else if (num53 == (ulong)(b3 - 4))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												num2 = b3;
												b2 = 5;
											}
											break;
										}
										if (decimal.Compare(d, 65074m) == 0)
										{
											b6 = 3;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												text3 = text3 + "[ディレイ" + Conversions.ToString(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]) + "(F)]";
												b2 = 0;
												b5 = 1;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
												break;
											}
											ulong num54 = num2;
											if (num54 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num54 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											break;
										}
										if (decimal.Compare(d, 65075m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "[FE33]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num55 = num2;
												if (num55 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65076m) == 0)
										{
											b6 = 4;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												text3 = text3 + "[FE34,アドレス0x" + $"{array2[1]:X4}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num56 = num2;
											if (num56 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num56 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num56 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											break;
										}
										if (decimal.Compare(d, 65077m) == 0)
										{
											b6 = 4;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												text3 = text3 + "[能力加算,種類0x" + $"{array2[1]:X2}" + ",+" + Conversions.ToString(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]) + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num57 = num2;
												if (num57 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num57 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num57 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65078m) == 0)
										{
											b6 = 4;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												text3 = text3 + "[能力減算,種類0x" + $"{array2[1]:X2}" + ",-" + Conversions.ToString(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]) + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num58 = num2;
												if (num58 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num58 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num58 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65079m) == 0)
										{
											b6 = 4;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												text3 = text3 + "[FE37,0x" + $"{array2[1]:X2}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num59 = num2;
												if (num59 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num59 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num59 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65081m) == 0)
										{
											b6 = 4;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												text3 = text3 + "[FE39,アドレス0x" + $"{array2[1]:X4}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num60 = num2;
											if (num60 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num60 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num60 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											break;
										}
										if (decimal.Compare(d, 65082m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "[能力変化精算]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num61 = num2;
												if (num61 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65083m) == 0)
										{
											b6 = 5;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												text3 = text3 + "[FE3B,アドレス0x" + $"{array2[1]:X4}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num62 = num2;
											if (num62 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num62 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num62 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num62 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											break;
										}
										if (decimal.Compare(d, 65084m) == 0)
										{
											b6 = 5;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												text3 = text3 + "[FE3C,アドレス0x" + $"{array2[1]:X4}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num63 = num2;
											if (num63 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num63 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num63 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num63 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											break;
										}
										if (decimal.Compare(d, 65085m) == 0)
										{
											b6 = 5;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												text3 = text3 + "[FE3D,アドレス0x" + $"{array2[1]:X4}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num64 = num2;
											if (num64 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num64 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num64 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num64 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											break;
										}
										if (decimal.Compare(d, 65086m) == 0)
										{
											b6 = 5;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												text3 = text3 + "[FE3E,アドレス0x" + $"{array2[1]:X4}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num65 = num2;
											if (num65 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num65 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num65 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num65 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											break;
										}
										if (decimal.Compare(d, 65087m) == 0)
										{
											b6 = 5;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												text3 = text3 + "[FE3F,アドレス0x" + $"{array2[1]:X4}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num66 = num2;
											if (num66 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num66 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num66 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num66 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											break;
										}
										if (decimal.Compare(d, 65088m) == 0)
										{
											b6 = 5;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												text3 = text3 + "[FE40,アドレス0x" + $"{array2[1]:X4}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num67 = num2;
											if (num67 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num67 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num67 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num67 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											break;
										}
										if (decimal.Compare(d, 65089m) == 0)
										{
											b6 = 5;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												text3 = text3 + "[能力書込,アドレス0x" + $"{array2[1]:X4}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num68 = num2;
											if (num68 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num68 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num68 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num68 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											break;
										}
										if (decimal.Compare(d, 65090m) == 0)
										{
											b6 = 4;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												text3 = text3 + "[FE42,0x" + $"{array2[1]:X2}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num69 = num2;
												if (num69 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num69 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num69 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65091m) == 0)
										{
											b6 = 4;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												text3 = text3 + "[FE43,0x" + $"{array2[1]:X2}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num70 = num2;
												if (num70 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num70 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num70 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65092m) == 0)
										{
											b6 = 4;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												text3 = text3 + "[FE44,0x" + $"{array2[1]:X2}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num71 = num2;
												if (num71 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num71 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num71 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65093m) == 0)
										{
											b6 = 4;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												text3 = text3 + "[FE45,0x" + $"{array2[1]:X2}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num72 = num2;
												if (num72 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num72 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num72 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65095m) == 0)
										{
											b6 = 5;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												text3 = text3 + "[FE47,アドレス0x" + $"{array2[1]:X4}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num73 = num2;
											if (num73 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num73 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num73 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num73 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											break;
										}
										if (decimal.Compare(d, 65096m) == 0)
										{
											b6 = 5;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												text3 = text3 + "[FE48,アドレス0x" + $"{array2[1]:X4}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num74 = num2;
											if (num74 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num74 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num74 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num74 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											break;
										}
										if (decimal.Compare(d, 65097m) == 0)
										{
											b6 = 5;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												text3 = text3 + "[FE49,アドレス0x" + $"{array2[1]:X4}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num75 = num2;
											if (num75 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num75 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num75 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num75 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											break;
										}
										if (decimal.Compare(d, 65098m) == 0)
										{
											b6 = 5;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												text3 = text3 + "[If分岐,アドレス0x" + $"{array2[1]:X4}" + "," + Conversions.ToString(array2[2]) + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num76 = num2;
											if (num76 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num76 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num76 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num76 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											break;
										}
										if (decimal.Compare(d, 65099m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "[Else]【";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num77 = num2;
												if (num77 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65100m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "】";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num78 = num2;
												if (num78 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65101m) == 0)
										{
											b6 = 5;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												text3 = text3 + "[FE4D,アドレス0x" + $"{array2[1]:X4}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num79 = num2;
											if (num79 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num79 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num79 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num79 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											break;
										}
										if (decimal.Compare(d, 65102m) == 0)
										{
											b6 = 5;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												text3 = text3 + "[FE4E,アドレス0x" + $"{array2[1]:X4}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num80 = num2;
											if (num80 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num80 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num80 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num80 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											break;
										}
										if (decimal.Compare(d, 65103m) == 0)
										{
											b6 = 5;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												text3 = text3 + "[FE4F,アドレス0x" + $"{array2[1]:X4}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num81 = num2;
											if (num81 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num81 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num81 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num81 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											break;
										}
										if (decimal.Compare(d, 65105m) == 0)
										{
											b6 = 5;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
												text3 = text3 + "[FE51,アドレス0x" + $"{array2[1]:X4}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num82 = num2;
											if (num82 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num82 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num82 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											else if (num82 == (ulong)(b3 - 3))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												num2 = b3;
												b2 = 4;
											}
											break;
										}
										if (decimal.Compare(d, 65107m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												text3 += "[希望球団]";
												b2 = 0;
												b5 = 1;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												break;
											}
											ulong num83 = num2;
											if (num83 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											break;
										}
										if (decimal.Compare(d, 65108m) == 0)
										{
											b6 = 4;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												text3 = text3 + "[FE54,0x" + $"{array2[1]:X2}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num84 = num2;
												if (num84 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num84 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num84 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65109m) == 0)
										{
											b6 = 4;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
												text3 = text3 + "[FE55,0x" + $"{array2[1]:X2}" + ",0x" + $"{array2[2]:X2}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num85 = num2;
												if (num85 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num85 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num85 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65110m) == 0)
										{
											b6 = 3;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												text3 = text3 + "[文字色" + Conversions.ToString(array2[1]) + "]";
												b2 = 0;
												b5 = 1;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
												break;
											}
											ulong num86 = num2;
											if (num86 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num86 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											break;
										}
										if (decimal.Compare(d, 65111m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "[スコア掲載]【";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num87 = num2;
												if (num87 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65112m) == 0)
										{
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "】";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num88 = num2;
												if (num88 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										if (decimal.Compare(d, 65113m) == 0)
										{
											b6 = 4;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
												text3 = text3 + "[FE59,アドレス0x" + $"{array2[1]:X4}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											ulong num89 = num2;
											if (num89 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num89 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											else if (num89 == (ulong)(b3 - 2))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
												num2 = b3;
												b2 = 3;
											}
											break;
										}
										b6 = 2;
										if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
										{
											if (unchecked(b5 == 1 && b == 0))
											{
												text3 += "\r\n";
												b5 = 0;
											}
											array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[(int)num2]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))])));
											text3 = text3 + "[" + $"{array2[1]:X4}" + "]";
											b2 = 0;
											num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
											if (b == 0)
											{
												text3 += "\r\n";
											}
										}
										else
										{
											ulong num90 = num2;
											if (num90 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
										}
										break;
									}
									case 255uL:
										if (unchecked(b5 == 1 && b == 0))
										{
											text3 += "\r\n";
											b5 = 0;
										}
										text3 += "[終端]";
										b2 = 0;
										if (b == 0)
										{
											text3 += "\r\n";
										}
										break;
									}
								}
								if (b != 0)
								{
									text3 += "\r\n";
								}
								if ((decimal.Compare(new decimal(num8), 1m) >= 0) & (Operators.CompareString(Strings.Mid(text3, Convert.ToInt32(decimal.Add(new decimal(value), 1m)), 16), "\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000", TextCompare: false) != 0))
								{
									text += text3;
									Application.DoEvents();
								}
							}
							Text = "処理データ:" + Conversions.ToString(num7) + "/" + Conversions.ToString(num6) + " 蓄積データ:" + Conversions.ToString(num3) + "/" + Conversions.ToString(蓄積データ出力NumericUpDown.Value) + " 処理中アドレス:" + Strings.Mid(str, 1, 8);
							Update();
							処理進行状況.Value = (int)Conversion.Int((double)num7 / (double)num6 * 100.0);
							経過表示Label.Text = Conversions.ToString(Conversion.Int((double)num7 / (double)num6 * 100.0)) + "%";
							if (decimal.Compare(new decimal(num3), 蓄積データ出力NumericUpDown.Value) >= 0)
							{
								if (Operators.CompareString(text, "", TextCompare: false) != 0)
								{
									MyProject.Computer.FileSystem.WriteAllText(Strings.Replace(参照ファイル名表示.Text, ".DMP", "") + "(" + Conversions.ToString(num4) + ").txt", text, append: false);
									num4 = Convert.ToUInt64(decimal.Add(new decimal(num4), 1m));
									text = "";
								}
								num3 = 0uL;
								Application.DoEvents();
							}
							num = Convert.ToUInt64(Wait時間NumericUpDown.Value);
							if (decimal.Compare(new decimal(value2), 3m) >= 0)
							{
								num7 = Convert.ToUInt64(decimal.Add(new decimal(num7), 1m));
							}
							if (decimal.Compare(decimal.Remainder(new decimal(value2), Wait間隔NumericUpDown.Value), 0m) == 0)
							{
								Thread.Sleep((int)num);
							}
							if ((decimal.Compare(new decimal(num8), 1m) >= 0) & (Operators.CompareString(Strings.Mid(text3, Convert.ToInt32(decimal.Add(new decimal(value), 1m)), 16), "\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000", TextCompare: false) != 0))
							{
								num3 = Convert.ToUInt64(decimal.Add(new decimal(num3), 1m));
							}
							else
							{
								value3 = Convert.ToUInt64(decimal.Add(new decimal(value3), 1m));
							}
							if (decimal.Compare(new decimal(value3), Wait間隔NumericUpDown.Value) == 0)
							{
								value3 = 0uL;
								Thread.Sleep((int)num);
							}
							if (Operators.CompareString(実行.Text, "実行", TextCompare: false) == 0)
							{
								goto end_IL_9dc5;
							}
							Application.DoEvents();
						}
						value2 = Convert.ToUInt64(decimal.Add(new decimal(value2), 1m));
						Application.DoEvents();
						continue;
						end_IL_9dc5:
						break;
					}
					Application.DoEvents();
					if (Operators.CompareString(text, "", TextCompare: false) != 0)
					{
						MyProject.Computer.FileSystem.WriteAllText(Strings.Replace(参照ファイル名表示.Text, ".DMP", "") + "(" + Conversions.ToString(num4) + ").txt", text, append: false);
					}
				}
				Application.DoEvents();
				出力オプションGroupBox.Enabled = true;
				文字コード選択ComboBox.Enabled = true;
				参照ファイル名表示.Enabled = true;
				参照.Enabled = true;
				Text = "変換終了";
			}
		}

		public void ポケ3以降の文字コード変換処理()
		{
			checked
			{
				if (MyProject.Computer.FileSystem.FileExists(参照ファイル名表示.Text))
				{
					出力オプションGroupBox.Enabled = false;
					文字コード選択ComboBox.Enabled = false;
					参照ファイル名表示.Enabled = false;
					参照.Enabled = false;
					using TextFieldParser textFieldParser = new TextFieldParser(参照ファイル名表示.Text);
					ulong[] array = new ulong[51];
					long[] array2 = new long[4];
					byte[] array3 = new byte[17];
					string[] array4 = new string[18];
					string[] array5 = new string[5];
					byte b = 0;
					if (アドレスありCheckBox.Checked)
					{
						b++;
					}
					if (十六進データありCheckBox.Checked)
					{
						b += 2;
					}
					if (アドレス化表示CheckBox.Checked)
					{
						b += 4;
					}
					ulong num = Convert.ToUInt64(Wait時間NumericUpDown.Value);
					int selectedIndex = 文字コード選択ComboBox.SelectedIndex;
					if (selectedIndex >= 2 && selectedIndex <= 4)
					{
						array4[1] = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉっゃゅょがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンヴァィゥェォッャュョガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ♂♀◎○★＠→←↑↓。、…「」＋ー？！『』～❤×・／（）％￥㎞㎏・・";
					}
					else if (selectedIndex >= 5 && selectedIndex <= 16)
					{
						array4[1] = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉっゃゅょがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンヴァィゥェォッャュョガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ♂♀◎○★＠→←↑↓。、…「」＋ー？！『』～❤×・／（）％￥♪♫・・";
					}
					else if (selectedIndex == 17)
					{
						array4[1] = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉっゃゅょがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンヴァィゥェォッャュョガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ♂♀◎○★＠→←↑↓。、…「」＋ー？！『』～❤×・／（）％￥♪♫贊・";
					}
					array4[17] = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜｦﾝｳｧｨｩｪｫｯｬｭｮｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾊﾋﾌﾍﾎﾊﾋﾌﾍﾎ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_+ｰ?!･｢｣/abcdefghijklmnopqrstuvwxyz⁰¹²³⁴⁵⁶⁷⁸⁹                                                                                              ";
					array4[2] = "亜唖娃阿哀愛挨姶逢葵茜穐悪握渥旭葦芦鯵梓圧斡扱宛姐虻飴絢綾鮎或粟袷安庵按暗案闇鞍杏以伊位依偉囲夷委威尉惟意慰易椅為畏異移維緯胃萎衣謂違遺医井亥域育郁磯一壱溢逸稲茨芋鰯允印咽員因姻引飲淫胤蔭院陰隠韻吋右宇烏羽迂雨卯鵜窺丑碓臼渦嘘唄欝蔚鰻姥厩浦瓜閏噂云運雲荏餌叡営嬰影映曳栄永泳洩瑛盈穎頴英衛詠鋭液疫益駅悦謁越閲榎厭円園堰奄宴延怨掩援沿演炎焔煙燕猿縁艶苑薗遠鉛鴛塩於汚甥凹央奥往応押旺横欧殴王翁襖鴬鴎黄岡沖荻億屋憶臆桶牡乙俺卸恩温穏音下化仮何伽価佳加可嘉夏嫁家寡科暇果架歌河火珂禍禾稼箇花苛茄荷華菓蝦課嘩貨迦過霞蚊俄";
					array4[3] = "峨我牙画臥芽蛾賀雅餓駕介会解回塊壊廻快怪悔恢懐戒拐改魁晦械海灰界皆絵芥蟹開階貝凱劾外咳害崖慨概涯碍蓋街該鎧骸浬馨蛙垣柿蛎鈎劃嚇各廓拡撹格核殻獲確穫覚角赫較郭閣隔革学岳楽額顎掛笠樫橿梶鰍潟割喝恰括活渇滑葛褐轄且鰹叶椛樺鞄株兜竃蒲釜鎌噛鴨栢茅萱粥刈苅瓦乾侃冠寒刊勘勧巻喚堪姦完官寛干幹患感慣憾換敢柑桓棺款歓汗漢澗潅環甘監看竿管簡緩缶翰肝艦莞観諌貫還鑑間閑関陥韓館舘丸含岸巌玩癌眼岩翫贋雁頑顔願企伎危喜器基奇嬉寄岐希幾忌揮机旗既期棋棄機帰毅気汽畿祈季稀紀徽規記貴起軌輝飢騎鬼亀偽儀妓宜戯技擬欺犠疑祇義蟻誼議掬菊鞠吉吃喫";
					array4[4] = "桔橘詰砧杵黍却客脚虐逆丘久仇休及吸宮弓急救朽求汲泣灸球究窮笈級糾給旧牛去居巨拒拠挙渠虚許距鋸漁禦魚亨享京供侠僑兇競共凶協匡卿叫喬境峡強彊怯恐恭挟教橋況狂狭矯胸脅興蕎郷鏡響饗驚仰凝尭暁業局曲極玉桐粁僅勤均巾錦斤欣欽琴禁禽筋緊芹菌衿襟謹近金吟銀九倶句区狗玖矩苦躯駆駈駒具愚虞喰空偶寓遇隅串櫛釧屑屈掘窟沓靴轡窪熊隈粂栗繰桑鍬勲君薫訓群軍郡卦袈祁係傾刑兄啓圭珪型契形径恵慶慧憩掲携敬景桂渓畦稽系経継繋罫茎荊蛍計詣警軽頚鶏芸迎鯨劇戟撃激隙桁傑欠決潔穴結血訣月件倹倦健兼券剣喧圏堅嫌建憲懸拳捲検権牽犬献研硯絹県肩見謙賢軒遣鍵";
					array4[5] = "険顕験鹸元原厳幻弦減源玄現絃舷言諺限乎個古呼固姑孤己庫弧戸故枯湖狐糊袴股胡菰虎誇跨鈷雇顧鼓五互伍午呉吾娯後御悟梧檎瑚碁語誤護醐乞鯉交佼侯候倖光公功効勾厚口向后喉坑垢好孔孝宏工巧巷幸広庚康弘恒慌抗拘控攻昂晃更杭校梗構江洪浩港溝甲皇硬稿糠紅紘絞綱耕考肯肱腔膏航荒行衡講貢購郊酵鉱砿鋼閤降項香高鴻剛劫号合壕拷濠豪轟麹克刻告国穀酷鵠黒獄漉腰甑忽惚骨狛込此頃今困坤墾婚恨懇昏昆根梱混痕紺艮魂些佐叉唆嵯左差査沙瑳砂詐鎖裟坐座挫債催再最哉塞妻宰彩才採栽歳済災采犀砕砦祭斎細菜裁載際剤在材罪財冴坂阪堺榊肴咲崎埼碕鷺作削咋搾昨朔柵";
					array4[6] = "窄策索錯桜鮭笹匙冊刷察拶撮擦札殺薩雑皐鯖捌錆鮫皿晒三傘参山惨撒散桟燦珊産算纂蚕讃賛酸餐斬暫残仕仔伺使刺司史嗣四士始姉姿子屍市師志思指支孜斯施旨枝止死氏獅祉私糸紙紫肢脂至視詞詩試誌諮資賜雌飼歯事似侍児字寺慈持時次滋治爾璽痔磁示而耳自蒔辞汐鹿式識鴫竺軸宍雫七叱執失嫉室悉湿漆疾質実蔀篠偲柴芝屡蕊縞舎写射捨赦斜煮社紗者謝車遮蛇邪借勺尺杓灼爵酌釈錫若寂弱惹主取守手朱殊狩珠種腫趣酒首儒受呪寿授樹綬需囚収周宗就州修愁拾洲秀秋終繍習臭舟蒐衆襲讐蹴輯週酋酬集醜什住充十従戎柔汁渋獣縦重銃叔夙宿淑祝縮粛塾熟出術述俊峻春瞬竣舜駿准";
					array4[7] = "循旬楯殉淳準潤盾純巡遵醇順処初所暑曙渚庶緒署書薯藷諸助叙女序徐恕鋤除傷償勝匠升召哨商唱嘗奨妾娼宵将小少尚庄床廠彰承抄招掌捷昇昌昭晶松梢樟樵沼消渉湘焼焦照症省硝礁祥称章笑粧紹肖菖蒋蕉衝裳訟証詔詳象賞醤鉦鍾鐘障鞘上丈丞乗冗剰城場壌嬢常情擾条杖浄状畳穣蒸譲醸錠嘱埴飾拭植殖燭織職色触食蝕辱尻伸信侵唇娠寝審心慎振新晋森榛浸深申疹真神秦紳臣芯薪親診身辛進針震人仁刃塵壬尋甚尽腎訊迅陣靭笥諏須酢図厨逗吹垂帥推水炊睡粋翠衰遂酔錐錘随瑞髄崇嵩数枢趨雛据杉椙菅頗雀裾澄摺寸世瀬畝是凄制勢姓征性成政整星晴棲栖正清牲生盛精聖声製西誠誓";
					array4[8] = "請逝醒青静斉税脆隻席惜戚斥昔析石積籍績脊責赤跡蹟碩切拙接摂折設窃節説雪絶舌蝉仙先千占宣専尖川戦扇撰栓栴泉浅洗染潜煎煽旋穿箭線繊羨腺舛船薦詮賎践選遷銭銑閃鮮前善漸然全禅繕膳糎噌塑岨措曾曽楚狙疏疎礎祖租粗素組蘇訴阻遡鼠僧創双叢倉喪壮奏爽宋層匝惣想捜掃挿掻操早曹巣槍槽漕燥争痩相窓糟総綜聡草荘葬蒼藻装走送遭鎗霜騒像増憎臓蔵贈造促側則即息捉束測足速俗属賊族続卒袖其揃存孫尊損村遜他多太汰詑唾堕妥惰打柁舵楕陀駄騨体堆対耐岱帯待怠態戴替泰滞胎腿苔袋貸退逮隊黛鯛代台大第醍題鷹滝瀧卓啄宅托択拓沢濯琢託鐸濁諾茸凧蛸只叩但達辰奪脱";
					array4[9] = "巽竪辿棚谷狸鱈樽誰丹単嘆坦担探旦歎淡湛炭短端箪綻耽胆蛋誕鍛団壇弾断暖檀段男談値知地弛恥智池痴稚置致蜘遅馳築畜竹筑蓄逐秩窒茶嫡着中仲宙忠抽昼柱注虫衷註酎鋳駐樗瀦猪苧著貯丁兆凋喋寵帖帳庁弔張彫徴懲挑暢朝潮牒町眺聴脹腸蝶調諜超跳銚長頂鳥勅捗直朕沈珍賃鎮陳津墜椎槌追鎚痛通塚栂掴槻佃漬柘辻蔦綴鍔椿潰坪壷嬬紬爪吊釣鶴亭低停偵剃貞呈堤定帝底庭廷弟悌抵挺提梯汀碇禎程締艇訂諦蹄逓邸鄭釘鼎泥摘擢敵滴的笛適鏑溺哲徹撤轍迭鉄典填天展店添纏甜貼転顛点伝殿澱田電兎吐堵塗妬屠徒斗杜渡登菟賭途都鍍砥砺努度土奴怒倒党冬凍刀唐塔塘套宕島嶋悼投";
					array4[10] = "搭東桃梼棟盗淘湯涛灯燈当痘祷等答筒糖統到董蕩藤討謄豆踏逃透鐙陶頭騰闘働動同堂導憧撞洞瞳童胴萄道銅峠鴇匿得徳涜特督禿篤毒独読栃橡凸突椴届鳶苫寅酉瀞噸屯惇敦沌豚遁頓呑曇鈍奈那内乍凪薙謎灘捺鍋楢馴縄畷南楠軟難汝二尼弐迩匂賑肉虹廿日乳入如尿韮任妊忍認濡禰祢寧葱猫熱年念捻撚燃粘乃廼之埜嚢悩濃納能脳膿農覗蚤巴把播覇杷波派琶破婆罵芭馬俳廃拝排敗杯盃牌背肺輩配倍培媒梅楳煤狽買売賠陪這蝿秤矧萩伯剥博拍柏泊白箔粕舶薄迫曝漠爆縛莫駁麦函箱硲箸肇筈櫨幡肌畑畠八鉢溌発醗髪伐罰抜筏閥鳩噺塙蛤隼伴判半反叛帆搬斑板氾汎版犯班畔繁般藩販範釆";
					array4[11] = "煩頒飯挽晩番盤磐蕃蛮匪卑否妃庇彼悲扉批披斐比泌疲皮碑秘緋罷肥被誹費避非飛樋簸備尾微枇毘琵眉美鼻柊稗匹疋髭彦膝菱肘弼必畢筆逼桧姫媛紐百謬俵彪標氷漂瓢票表評豹廟描病秒苗錨鋲蒜蛭鰭品彬斌浜瀕貧賓頻敏瓶不付埠夫婦富冨布府怖扶敷斧普浮父符腐膚芙譜負賦赴阜附侮撫武舞葡蕪部封楓風葺蕗伏副復幅服福腹複覆淵弗払沸仏物鮒分吻噴墳憤扮焚奮粉糞紛雰文聞丙併兵塀幣平弊柄並蔽閉陛米頁僻壁癖碧別瞥蔑箆偏変片篇編辺返遍便勉娩弁鞭保舗鋪圃捕歩甫補輔穂募墓慕戊暮母簿菩倣俸包呆報奉宝峰峯崩庖抱捧放方朋法泡烹砲縫胞芳萌蓬蜂褒訪豊邦鋒飽鳳鵬乏亡傍剖";
					array4[12] = "坊妨帽忘忙房暴望某棒冒紡肪膨謀貌貿鉾防吠頬北僕卜墨撲朴牧睦穆釦勃没殆堀幌奔本翻凡盆・摩磨魔麻埋妹昧枚毎哩槙幕膜枕鮪柾鱒桝亦俣又抹末沫迄侭繭麿万慢満漫蔓味未魅巳箕岬密蜜湊蓑稔脈妙粍民眠務夢無牟矛霧鵡椋婿娘冥名命明盟迷銘鳴姪牝滅免棉綿緬面麺摸模茂妄孟毛猛盲網耗蒙儲木黙目杢勿餅尤戻籾貰問悶紋門匁也冶夜爺耶野弥矢厄役約薬訳躍靖柳薮鑓愉愈油癒諭輸唯佑優勇友宥幽悠憂揖有柚湧涌猶猷由祐裕誘遊邑郵雄融夕予余与誉輿預傭幼妖容庸揚揺擁曜楊様洋溶熔用窯羊耀葉蓉要謡踊遥陽養慾抑欲沃浴翌翼淀羅螺裸来莱頼雷洛絡落酪乱卵嵐欄濫藍蘭覧利吏";
					array4[13] = "履李梨理璃痢裏裡里離陸律率立葎掠略劉流溜琉留硫粒隆竜龍侶慮旅虜了亮僚両凌寮料梁涼猟療瞭稜糧良諒遼量陵領力緑倫厘林淋燐琳臨輪隣鱗麟瑠塁涙累類令伶例冷励嶺怜玲礼苓鈴隷零霊麗齢暦歴列劣烈裂廉恋憐漣煉簾練聯蓮連錬呂魯櫓炉賂路露労婁廊弄朗楼榔浪漏牢狼篭老聾蝋郎六麓禄肋録論倭和話歪賄脇惑枠鷲亙亘鰐詫藁蕨椀湾碗腕々\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000丼亞仗伉佗佇佛伜俶俯會偸傀傴傲儂儚儡儺冕冤冦冩冲凉凛几凭凰刎刧刮刹剋剌剴劔辧勁匈匐匣卍卷厠咀咬哈咤哦唏唔哭啗嘔嘖墫壺壻奢埃娑娚媚";
					array4[14] = "尅將屁嶌崋崑崔廣弩彗徂彿忿怱恚恷舉暝曄曚朦霸杞杠柩枸檜桍梟梵棕楜洟浣涅淹渕淆淒淮溽溯潯潭澡澤澪濱瀉瀰灑炬炸烙焙犂犒狢狡狹猜猥獏獨珀琲瑜璋璧瓔珱畸當疵慮眸睇瞑矮砌磋祀祠祗祟笘筐筧篏籔籬籵糅經綺綮綣罸羂聚肛肓肚胚胱脛腋苳苺茹茫茗莵荳荵莉菘萋菲萠蒄葫萬蒹蔔蓼薔藪蕾號蛄蛟蛛蜥蠱衒袒袙裃裼褌褪褝覬訃訖詭詬詢誅誂諚諫踵蹉踪躬躰躾軋迪遑遒邨邯邱邵郢郤釡閠隹餃饅駝遙瑤昻\u3000珉\u3000\u3000緖逸郞鄕鄧\u3000\u3000\u3000\u3000\u3000あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉっゃゅょがぎぐげござじずぜ";
					int selectedIndex2 = 文字コード選択ComboBox.SelectedIndex;
					if (selectedIndex2 >= 2 && selectedIndex2 <= 12)
					{
						array4[15] = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉっゃゅょがぎぐげござじずぜあいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉっゃゅょがぎぐげござじずぜあいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉっゃゅょがぎぐげござじずぜあいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉっゃゅょがぎぐげござじずぜ";
						array4[16] = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉっゃゅょがぎぐげござじずぜあいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉっゃゅょがぎぐげござじずぜあいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉっゃゅょがぎぐげござじずぜあいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉっゃゅょがぎぐげござじずぜ";
					}
					else if (selectedIndex2 >= 13 && selectedIndex2 <= 17)
					{
						array4[15] = "ⒶⒷⓍⓎⓁⓇ✛\u3000\u3000\u3000\u3000\u3000☀☁☂☃  ☎✉⊞♠♦♥♣→←↑↓× !″＃$%&'()*＋,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[〵]^_'abcdefghijklmnopqrstuvwxyz｛|｝~€.\u00a8…^Œ′′″″●″™≻œ¡¢£\u00a8©®°±\u00b4+¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüý 、。，．･：；？！\u309b\u309c′‵\u00a8^\uffe3\uff3fゝヾ々‒—–／＼～❘…‘'″″（）〔〕［］｛｝＜＞「";
						array4[16] = "」+-±×÷=∞∴°′″＆☆★○●◎◇◆□■△▲▼▼※〒→←↑↓♯♭♪ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶ\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000";
					}
					ulong num2 = 0uL;
					ulong value = 0uL;
					ulong value2 = 1uL;
					ulong num3 = 1uL;
					ulong value3 = 0uL;
					ulong num4 = 1uL;
					ulong num5 = 1uL;
					処理進行状況.Value = 0;
					ulong num6 = Convert.ToUInt64(decimal.Subtract(new decimal(GetLinesOfTextFile(参照ファイル名表示.Text)), 2m));
					ulong num7 = 1uL;
					string str = "";
					string text = "";
					byte b2 = 0;
					byte b3 = 0;
					byte b4 = 0;
					array5[1] = "";
					array5[2] = "";
					array5[3] = "";
					array5[4] = "";
					byte b5 = 0;
					textFieldParser.TextFieldType = FieldType.Delimited;
					textFieldParser.SetDelimiters("区切りなし");
					ulong num8 = default(ulong);
					while (!textFieldParser.EndOfData)
					{
						string[] array6 = textFieldParser.ReadFields();
						string[] array7 = array6;
						foreach (string text2 in array7)
						{
							string text3 = text2;
							if (decimal.Compare(new decimal(value2), 3m) >= 0)
							{
								if (Operators.CompareString(Strings.Mid(text3, 11, 2), "  ", TextCompare: false) != 0)
								{
									array3[1] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 11, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 14, 2), "  ", TextCompare: false) != 0)
								{
									array3[2] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 14, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 17, 2), "  ", TextCompare: false) != 0)
								{
									array3[3] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 17, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 20, 2), "  ", TextCompare: false) != 0)
								{
									array3[4] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 20, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 23, 2), "  ", TextCompare: false) != 0)
								{
									array3[5] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 23, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 26, 2), "  ", TextCompare: false) != 0)
								{
									array3[6] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 26, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 29, 2), "  ", TextCompare: false) != 0)
								{
									array3[7] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 29, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 32, 2), "  ", TextCompare: false) != 0)
								{
									array3[8] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 32, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 35, 2), "  ", TextCompare: false) != 0)
								{
									array3[9] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 35, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 38, 2), "  ", TextCompare: false) != 0)
								{
									array3[10] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 38, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 41, 2), "  ", TextCompare: false) != 0)
								{
									array3[11] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 41, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 44, 2), "  ", TextCompare: false) != 0)
								{
									array3[12] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 44, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 47, 2), "  ", TextCompare: false) != 0)
								{
									array3[13] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 47, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 50, 2), "  ", TextCompare: false) != 0)
								{
									array3[14] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 50, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 53, 2), "  ", TextCompare: false) != 0)
								{
									array3[15] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 53, 2));
								}
								if (Operators.CompareString(Strings.Mid(text3, 56, 2), "  ", TextCompare: false) != 0)
								{
									array3[16] = (byte)Conversions.ToInteger("&H" + Strings.Mid(text3, 56, 2));
								}
								num8 = 0uL;
								num2 = 1uL;
								do
								{
									num8 += array3[(int)num2];
									Application.DoEvents();
									num2++;
								}
								while (num2 <= 16);
								str = text3;
								text3 = "";
								value = 0uL;
								if (アドレスありCheckBox.Checked)
								{
									text3 += Strings.Mid(str, 1, 10);
									value = Convert.ToUInt64(decimal.Add(new decimal(value), 10m));
								}
								if (十六進データありCheckBox.Checked)
								{
									text3 = text3 + Strings.Mid(str, 11, 47) + "  ";
									value = Convert.ToUInt64(decimal.Add(new decimal(value), 49m));
								}
								b3 = (byte)(b2 + 16);
								b4 = b2;
								num2 = 1uL;
								do
								{
									array[(int)(num2 + b2)] = array3[(int)num2];
									num2++;
								}
								while (num2 <= 16);
								ulong num9 = b3;
								for (num2 = 1uL; num2 <= num9; num2++)
								{
									ulong num10 = array[(int)num2];
									if (num10 == 0)
									{
										text3 += " ";
										b2 = 0;
										b5 = 1;
									}
									else if (num10 >= 1 && num10 <= 231)
									{
										text3 += Strings.Mid(array4[1], (int)array[(int)num2], 1);
										b2 = 0;
										b5 = 1;
									}
									else if (num10 >= 232 && num10 <= 247)
									{
										byte b6 = 2;
										if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
										{
											decimal d = decimal.Add(decimal.Multiply(new decimal(array[(int)num2]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))]));
											if (decimal.Compare(d, 62359m) == 0)
											{
												int selectedIndex3 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex3 == 2)
												{
													text3 += "・";
												}
												else if (selectedIndex3 >= 3 && selectedIndex3 <= 17)
												{
													text3 += "髙";
												}
											}
											else if (decimal.Compare(d, 62360m) == 0)
											{
												int selectedIndex4 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex4 == 2)
												{
													text3 += "・";
												}
												else if (selectedIndex4 >= 3 && selectedIndex4 <= 16)
												{
													text3 += "礒";
												}
												else if (selectedIndex4 == 17)
												{
													text3 += "ｶﾙ";
												}
											}
											else if (decimal.Compare(d, 62361m) == 0)
											{
												int selectedIndex5 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex5 == 2)
												{
													text3 += "・";
												}
												else if (selectedIndex5 >= 3 && selectedIndex5 <= 16)
												{
													text3 += "臺";
												}
												else if (selectedIndex5 == 17)
												{
													text3 += "ﾛｽ";
												}
											}
											else if (decimal.Compare(d, 62362m) == 0)
											{
												int selectedIndex6 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex6 == 2)
												{
													text3 += "・";
												}
												else if (selectedIndex6 >= 3 && selectedIndex6 <= 16)
												{
													text3 += "晟";
												}
												else if (selectedIndex6 == 17)
												{
													text3 += "ﾛ･";
												}
											}
											else if (decimal.Compare(d, 62363m) == 0)
											{
												int selectedIndex7 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex7 == 2)
												{
													text3 += "・";
												}
												else if (selectedIndex7 >= 3 && selectedIndex7 <= 16)
												{
													text3 += "﨑";
												}
												else if (selectedIndex7 == 17)
												{
													text3 += "ｻ";
												}
											}
											else if (decimal.Compare(d, 62364m) == 0)
											{
												int selectedIndex8 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex8 >= 2 && selectedIndex8 <= 4)
												{
													text3 += "・";
												}
												else if (selectedIndex8 >= 5 && selectedIndex8 <= 17)
												{
													text3 += "巫";
												}
											}
											else if (decimal.Compare(d, 62365m) == 0)
											{
												int selectedIndex9 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex9 >= 2 && selectedIndex9 <= 4)
												{
													text3 += "・";
												}
												else if (selectedIndex9 >= 5 && selectedIndex9 <= 17)
												{
													text3 += "脩";
												}
											}
											else if (decimal.Compare(d, 62365m) == 0)
											{
												int selectedIndex10 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex10 >= 2 && selectedIndex10 <= 4)
												{
													text3 += "・";
												}
												else if (selectedIndex10 >= 5 && selectedIndex10 <= 17)
												{
													text3 += "翔";
												}
											}
											else if (decimal.Compare(d, 62367m) == 0)
											{
												int selectedIndex11 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex11 >= 2 && selectedIndex11 <= 4)
												{
													text3 += "・";
												}
												else if (selectedIndex11 >= 5 && selectedIndex11 <= 17)
												{
													text3 += "圀";
												}
											}
											else if (decimal.Compare(d, 62368m) == 0)
											{
												int selectedIndex12 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex12 >= 2 && selectedIndex12 <= 4)
												{
													text3 += "・";
												}
												else if (selectedIndex12 >= 5 && selectedIndex12 <= 17)
												{
													text3 += "邉";
												}
											}
											else if (decimal.Compare(d, 62369m) == 0)
											{
												int selectedIndex13 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex13 >= 2 && selectedIndex13 <= 5)
												{
													text3 += "・";
												}
												else if (selectedIndex13 >= 6 && selectedIndex13 <= 17)
												{
													text3 += "燁";
												}
											}
											else if (decimal.Compare(d, 62370m) == 0)
											{
												int selectedIndex14 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex14 >= 2 && selectedIndex14 <= 5)
												{
													text3 += "・";
												}
												else if ((selectedIndex14 >= 6 && selectedIndex14 <= 8) || selectedIndex14 == 10)
												{
													text3 += "G･";
												}
												else if (selectedIndex14 == 9 || (selectedIndex14 >= 12 && selectedIndex14 <= 13))
												{
													text3 += " ﾌ";
												}
												else if (selectedIndex14 == 11)
												{
													text3 += "＃";
												}
												else if (selectedIndex14 >= 14 && selectedIndex14 <= 16)
												{
													text3 += "G.";
												}
												else if (selectedIndex14 == 17)
												{
													text3 += "枡";
												}
											}
											else if (decimal.Compare(d, 62371m) == 0)
											{
												int selectedIndex15 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex15 >= 2 && selectedIndex15 <= 5)
												{
													text3 += "・";
												}
												else if ((selectedIndex15 >= 6 && selectedIndex15 <= 8) || selectedIndex15 == 10)
												{
													text3 += "G･";
												}
												else if (selectedIndex15 == 9 || (selectedIndex15 >= 12 && selectedIndex15 <= 13))
												{
													text3 += "ｪﾘ";
												}
												else if (selectedIndex15 == 11)
												{
													text3 += "＄";
												}
												else if (selectedIndex15 >= 14 && selectedIndex15 <= 17)
												{
													text3 += "朗";
												}
											}
											else if (decimal.Compare(d, 62372m) == 0)
											{
												int selectedIndex16 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex16 >= 2 && selectedIndex16 <= 5)
												{
													text3 += "・";
												}
												else if ((selectedIndex16 >= 6 && selectedIndex16 <= 8) || selectedIndex16 == 10)
												{
													text3 += "佐";
												}
												else if (selectedIndex16 == 9 || (selectedIndex16 >= 12 && selectedIndex16 <= 13))
												{
													text3 += "ｼｱ";
												}
												else if (selectedIndex16 == 1)
												{
													text3 += "＆";
												}
												else if (selectedIndex16 >= 14 && selectedIndex16 <= 17)
												{
													text3 += "曉";
												}
											}
											else if (decimal.Compare(d, 62373m) == 0)
											{
												int selectedIndex17 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex17 >= 2 && selectedIndex17 <= 5)
												{
													text3 += "・";
												}
												else if ((selectedIndex17 >= 6 && selectedIndex17 <= 8) || selectedIndex17 == 10)
												{
													text3 += "藤";
												}
												else if (selectedIndex17 == 9 || (selectedIndex17 >= 12 && selectedIndex17 <= 13))
												{
													text3 += "ｰﾉ";
												}
												else if (selectedIndex17 == 11)
												{
													text3 += "＝";
												}
												else if (selectedIndex17 == 14)
												{
													text3 += "\u3000";
												}
												else if (selectedIndex17 >= 15 && selectedIndex17 <= 17)
												{
													text3 += "攝";
												}
											}
											else if (decimal.Compare(d, 62374m) == 0)
											{
												int selectedIndex18 = 文字コード選択ComboBox.SelectedIndex;
												if ((selectedIndex18 >= 2 && selectedIndex18 <= 8) || selectedIndex18 == 10)
												{
													text3 += "・";
												}
												else if (selectedIndex18 == 9 || (selectedIndex18 >= 12 && selectedIndex18 <= 17))
												{
													text3 += "MI";
												}
												else if (selectedIndex18 == 11)
												{
													text3 += "ａ";
												}
											}
											else if (decimal.Compare(d, 62375m) == 0)
											{
												int selectedIndex19 = 文字コード選択ComboBox.SelectedIndex;
												if ((selectedIndex19 >= 2 && selectedIndex19 <= 8) || selectedIndex19 == 10)
												{
													text3 += "・";
												}
												else if (selectedIndex19 == 9 || (selectedIndex19 >= 12 && selectedIndex19 <= 17))
												{
													text3 += "CH";
												}
												else if (selectedIndex19 == 11)
												{
													text3 += "ｂ";
												}
											}
											else if (decimal.Compare(d, 62376m) == 0)
											{
												int selectedIndex20 = 文字コード選択ComboBox.SelectedIndex;
												if ((selectedIndex20 >= 2 && selectedIndex20 <= 8) || selectedIndex20 == 10)
												{
													text3 += "・";
												}
												else if (selectedIndex20 == 9 || (selectedIndex20 >= 12 && selectedIndex20 <= 17))
												{
													text3 += "E";
												}
												else if (selectedIndex20 == 11)
												{
													text3 += "ｃ";
												}
											}
											else if (decimal.Compare(d, 62377m) == 0)
											{
												int selectedIndex21 = 文字コード選択ComboBox.SelectedIndex;
												if ((selectedIndex21 >= 2 && selectedIndex21 <= 8) || selectedIndex21 == 10)
												{
													text3 += "・";
												}
												else if (selectedIndex21 == 9 || (selectedIndex21 >= 12 && selectedIndex21 <= 17))
												{
													text3 += "AL";
												}
												else if (selectedIndex21 == 11)
												{
													text3 += "ｄ";
												}
											}
											else if (decimal.Compare(d, 62378m) == 0)
											{
												int selectedIndex22 = 文字コード選択ComboBox.SelectedIndex;
												if ((selectedIndex22 >= 2 && selectedIndex22 <= 8) || selectedIndex22 == 10)
												{
													text3 += "・";
												}
												else if (selectedIndex22 == 9)
												{
													text3 += "\u3000";
												}
												else if (selectedIndex22 >= 12 && selectedIndex22 <= 17)
												{
													text3 += "姜";
												}
												else if (selectedIndex22 == 11)
												{
													text3 += "ｅ";
												}
											}
											else if (decimal.Compare(d, 62379m) == 0)
											{
												int selectedIndex23 = 文字コード選択ComboBox.SelectedIndex;
												if ((selectedIndex23 >= 2 && selectedIndex23 <= 8) || selectedIndex23 == 10)
												{
													text3 += "・";
												}
												else if (selectedIndex23 == 9)
												{
													text3 += "\u3000";
												}
												else if (selectedIndex23 >= 12 && selectedIndex23 <= 17)
												{
													text3 += "秦";
												}
												else if (selectedIndex23 == 11)
												{
													text3 += "ｆ";
												}
											}
											else if (decimal.Compare(d, 62380m) == 0)
											{
												int selectedIndex24 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex24 >= 2 && selectedIndex24 <= 10)
												{
													text3 += "・";
												}
												else if (selectedIndex24 >= 12 && selectedIndex24 <= 17)
												{
													text3 += "邊";
												}
												else if (selectedIndex24 == 11)
												{
													text3 += "ｇ";
												}
											}
											else if (decimal.Compare(d, 62381m) == 0)
											{
												int selectedIndex25 = 文字コード選択ComboBox.SelectedIndex;
												if ((selectedIndex25 >= 2 && selectedIndex25 <= 10) || (selectedIndex25 >= 12 && selectedIndex25 <= 14))
												{
													text3 += "・";
												}
												else if (selectedIndex25 == 11)
												{
													text3 += "ｈ";
												}
												else if (selectedIndex25 >= 15 && selectedIndex25 <= 17)
												{
													text3 += "齊";
												}
											}
											else if (decimal.Compare(d, 62382m) == 0)
											{
												int selectedIndex26 = 文字コード選択ComboBox.SelectedIndex;
												if ((selectedIndex26 >= 2 && selectedIndex26 <= 10) || selectedIndex26 == 12)
												{
													text3 += "・";
												}
												else if (selectedIndex26 == 11)
												{
													text3 += "ｉ";
												}
												else if (selectedIndex26 >= 13 && selectedIndex26 <= 17)
												{
													text3 += "炳";
												}
											}
											else if (decimal.Compare(d, 62383m) == 0)
											{
												int selectedIndex27 = 文字コード選択ComboBox.SelectedIndex;
												if ((selectedIndex27 >= 2 && selectedIndex27 <= 10) || selectedIndex27 == 12)
												{
													text3 += "・";
												}
												else if (selectedIndex27 == 11)
												{
													text3 += "ｊ";
												}
												else if (selectedIndex27 >= 13 && selectedIndex27 <= 17)
												{
													text3 += "壽";
												}
											}
											else if (decimal.Compare(d, 62384m) == 0)
											{
												int selectedIndex28 = 文字コード選択ComboBox.SelectedIndex;
												if ((selectedIndex28 >= 2 && selectedIndex28 <= 10) || selectedIndex28 == 12)
												{
													text3 += "・";
												}
												else if (selectedIndex28 == 11)
												{
													text3 += "ｋ";
												}
												else if (selectedIndex28 >= 13 && selectedIndex28 <= 14)
												{
													text3 += "TS";
												}
												else if (selectedIndex28 >= 15 && selectedIndex28 <= 17)
												{
													text3 += "奎";
												}
											}
											else if (decimal.Compare(d, 62385m) == 0)
											{
												int selectedIndex29 = 文字コード選択ComboBox.SelectedIndex;
												if ((selectedIndex29 >= 2 && selectedIndex29 <= 10) || selectedIndex29 == 12)
												{
													text3 += "・";
												}
												else if (selectedIndex29 == 11)
												{
													text3 += "ｌ";
												}
												else if (selectedIndex29 >= 13 && selectedIndex29 <= 14)
												{
													text3 += "UY";
												}
												else if (selectedIndex29 >= 15 && selectedIndex29 <= 17)
												{
													text3 += "洸";
												}
											}
											else if (decimal.Compare(d, 62386m) == 0)
											{
												int selectedIndex30 = 文字コード選択ComboBox.SelectedIndex;
												if ((selectedIndex30 >= 2 && selectedIndex30 <= 10) || selectedIndex30 == 12)
												{
													text3 += "・";
												}
												else if (selectedIndex30 == 11)
												{
													text3 += "ｍ";
												}
												else if (selectedIndex30 >= 13 && selectedIndex30 <= 14)
												{
													text3 += "OS";
												}
												else if (selectedIndex30 >= 15 && selectedIndex30 <= 16)
												{
													text3 += "踐";
												}
												else if (selectedIndex30 == 17)
												{
													text3 += "眞";
												}
											}
											else if (decimal.Compare(d, 62387m) == 0)
											{
												int selectedIndex31 = 文字コード選択ComboBox.SelectedIndex;
												if ((selectedIndex31 >= 2 && selectedIndex31 <= 10) || selectedIndex31 == 12)
												{
													text3 += "・";
												}
												else if (selectedIndex31 == 11)
												{
													text3 += "ｎ";
												}
												else if (selectedIndex31 >= 13 && selectedIndex31 <= 14)
												{
													text3 += "HI";
												}
												else
												{
													switch (selectedIndex31)
													{
													case 15:
														text3 += "\u3000";
														break;
													case 16:
														text3 += "杋";
														break;
													case 17:
														text3 += "嵜";
														break;
													}
												}
											}
											else if (decimal.Compare(d, 62388m) == 0)
											{
												int selectedIndex32 = 文字コード選択ComboBox.SelectedIndex;
												if ((selectedIndex32 >= 2 && selectedIndex32 <= 10) || selectedIndex32 == 12)
												{
													text3 += "・";
												}
												else if (selectedIndex32 == 11)
												{
													text3 += "ｏ";
												}
												else if (selectedIndex32 >= 13 && selectedIndex32 <= 17)
												{
													text3 += "ｸﾞﾗ";
												}
											}
											else if (decimal.Compare(d, 62389m) == 0)
											{
												int selectedIndex33 = 文字コード選択ComboBox.SelectedIndex;
												if ((selectedIndex33 >= 2 && selectedIndex33 <= 10) || selectedIndex33 == 12)
												{
													text3 += "・";
												}
												else if (selectedIndex33 == 11)
												{
													text3 += "ｐ";
												}
												else if (selectedIndex33 >= 13 && selectedIndex33 <= 17)
												{
													text3 += "ｲｼ";
												}
											}
											else if (decimal.Compare(d, 62390m) == 0)
											{
												int selectedIndex34 = 文字コード選択ComboBox.SelectedIndex;
												if ((selectedIndex34 >= 2 && selectedIndex34 <= 10) || selectedIndex34 == 12)
												{
													text3 += "・";
												}
												else if (selectedIndex34 == 11)
												{
													text3 += "ｑ";
												}
												else if (selectedIndex34 >= 13 && selectedIndex34 <= 17)
												{
													text3 += "ﾝｶ";
												}
											}
											else if (decimal.Compare(d, 62391m) == 0)
											{
												int selectedIndex35 = 文字コード選択ComboBox.SelectedIndex;
												if ((selectedIndex35 >= 2 && selectedIndex35 <= 10) || selectedIndex35 == 12)
												{
													text3 += "・";
												}
												else if (selectedIndex35 == 11)
												{
													text3 += "ｒ";
												}
												else if (selectedIndex35 >= 13 && selectedIndex35 <= 17)
												{
													text3 += "ﾞｰ";
												}
											}
											else if (decimal.Compare(d, 62392m) == 0)
											{
												int selectedIndex36 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex36 >= 2 && selectedIndex36 <= 5)
												{
													text3 += "・";
												}
												else if ((selectedIndex36 >= 6 && selectedIndex36 <= 10) || (selectedIndex36 >= 12 && selectedIndex36 <= 14))
												{
													text3 += "ﾌｪ";
												}
												else if (selectedIndex36 == 11)
												{
													text3 += "ｓ";
												}
												else if (selectedIndex36 >= 15 && selectedIndex36 <= 17)
												{
													text3 += "ﾌｧ";
												}
											}
											else if (decimal.Compare(d, 62393m) == 0)
											{
												int selectedIndex37 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex37 >= 2 && selectedIndex37 <= 5)
												{
													text3 += "・";
												}
												else if ((selectedIndex37 >= 6 && selectedIndex37 <= 10) || (selectedIndex37 >= 12 && selectedIndex37 <= 14))
												{
													text3 += "ﾙﾅ";
												}
												else if (selectedIndex37 == 11)
												{
													text3 += "ｔ";
												}
												else if (selectedIndex37 >= 15 && selectedIndex37 <= 17)
												{
													text3 += "ﾙｹ";
												}
											}
											else if (decimal.Compare(d, 62394m) == 0)
											{
												int selectedIndex38 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex38 >= 2 && selectedIndex38 <= 5)
												{
													text3 += "・";
												}
												else if ((selectedIndex38 >= 6 && selectedIndex38 <= 10) || (selectedIndex38 >= 12 && selectedIndex38 <= 14))
												{
													text3 += "ﾝﾃ";
												}
												else if (selectedIndex38 == 11)
												{
													text3 += "ｕ";
												}
												else if (selectedIndex38 >= 15 && selectedIndex38 <= 17)
												{
													text3 += "ﾝﾎﾞ";
												}
											}
											else if (decimal.Compare(d, 62395m) == 0)
											{
												int selectedIndex39 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex39 >= 2 && selectedIndex39 <= 5)
												{
													text3 += "・";
												}
												else if ((selectedIndex39 >= 6 && selectedIndex39 <= 10) || (selectedIndex39 >= 12 && selectedIndex39 <= 14))
												{
													text3 += "ﾞｽ";
												}
												else if (selectedIndex39 == 11)
												{
													text3 += "ｖ";
												}
												else if (selectedIndex39 >= 15 && selectedIndex39 <= 17)
												{
													text3 += "ｰｸﾞ";
												}
											}
											else if (decimal.Compare(d, 62396m) == 0)
											{
												int selectedIndex40 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex40 >= 2 && selectedIndex40 <= 5)
												{
													text3 += "・";
												}
												else if ((selectedIndex40 >= 6 && selectedIndex40 <= 10) || (selectedIndex40 >= 12 && selectedIndex40 <= 14))
												{
													text3 += "ﾌｪ";
												}
												else if (selectedIndex40 == 11)
												{
													text3 += "ｗ";
												}
												else if (selectedIndex40 == 15)
												{
													text3 += "ﾊﾞ";
												}
												else if (selectedIndex40 >= 16 && selectedIndex40 <= 17)
												{
													text3 += "ﾒｯ";
												}
											}
											else if (decimal.Compare(d, 62397m) == 0)
											{
												int selectedIndex41 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex41 >= 2 && selectedIndex41 <= 5)
												{
													text3 += "・";
												}
												else if ((selectedIndex41 >= 5 && selectedIndex41 <= 10) || (selectedIndex41 >= 12 && selectedIndex41 <= 14))
												{
													text3 += "ﾙﾅ";
												}
												else if (selectedIndex41 == 11)
												{
													text3 += "ｘ";
												}
												else if (selectedIndex41 == 15)
												{
													text3 += "ｰﾅ";
												}
												else if (selectedIndex41 >= 16 && selectedIndex41 <= 17)
												{
													text3 += "ｾﾝ";
												}
											}
											else if (decimal.Compare(d, 62398m) == 0)
											{
												int selectedIndex42 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex42 >= 2 && selectedIndex42 <= 5)
												{
													text3 += "・";
												}
												else if ((selectedIndex42 >= 6 && selectedIndex42 <= 10) || (selectedIndex42 >= 12 && selectedIndex42 <= 14))
												{
													text3 += "ﾝﾃ";
												}
												else if (selectedIndex42 == 11)
												{
													text3 += "ｙ";
												}
												else if (selectedIndex42 == 15)
												{
													text3 += "ﾑJ";
												}
												else if (selectedIndex42 >= 16 && selectedIndex42 <= 17)
												{
													text3 += "ｼﾞ";
												}
											}
											else if (decimal.Compare(d, 62399m) == 0)
											{
												int selectedIndex43 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex43 >= 2 && selectedIndex43 <= 5)
												{
													text3 += "・";
												}
												else if ((selectedIndex43 >= 6 && selectedIndex43 <= 10) || (selectedIndex43 >= 12 && selectedIndex43 <= 14))
												{
													text3 += "ﾞｽ";
												}
												else if (selectedIndex43 == 11)
												{
													text3 += "ｚ";
												}
												else if (selectedIndex43 == 15)
												{
													text3 += "r.";
												}
												else if (selectedIndex43 >= 16 && selectedIndex43 <= 17)
												{
													text3 += "ｬｰ";
												}
											}
											else if (decimal.Compare(d, 62642m) == 0)
											{
												int selectedIndex44 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex44 >= 2 && selectedIndex44 <= 12)
												{
													text3 += "朗";
												}
												else if (selectedIndex44 >= 13 && selectedIndex44 <= 17)
												{
													text3 += "朗";
												}
											}
											else if (decimal.Compare(d, 62644m) == 0)
											{
												int selectedIndex45 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex45 >= 2 && selectedIndex45 <= 16)
												{
													text3 += "珣";
												}
												else if (selectedIndex45 == 17)
												{
													text3 += "﨑";
												}
											}
											else if (decimal.Compare(d, 62645m) == 0)
											{
												int selectedIndex46 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex46 >= 2 && selectedIndex46 <= 16)
												{
													text3 += "實";
												}
												else if (selectedIndex46 == 17)
												{
													text3 += "颯";
												}
											}
											else if (decimal.Compare(d, 62651m) == 0)
											{
												int selectedIndex47 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex47 >= 2 && selectedIndex47 <= 4)
												{
													text3 += "ｼｭ";
												}
												else if ((selectedIndex47 >= 5 && selectedIndex47 <= 10) || (selectedIndex47 >= 12 && selectedIndex47 <= 17))
												{
													text3 += "ﾌｪ";
												}
												else if (selectedIndex47 == 11)
												{
													text3 += "｜";
												}
											}
											else if (decimal.Compare(d, 62652m) == 0)
											{
												int selectedIndex48 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex48 >= 2 && selectedIndex48 <= 4)
												{
													text3 += "ｰﾙ";
												}
												else if ((selectedIndex48 >= 5 && selectedIndex48 <= 10) || (selectedIndex48 >= 12 && selectedIndex48 <= 17))
												{
													text3 += "ﾙﾅ";
												}
												else if (selectedIndex48 == 11)
												{
													text3 += "\uff3f";
												}
											}
											else if (decimal.Compare(d, 62653m) == 0)
											{
												int selectedIndex49 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex49 >= 2 && selectedIndex49 <= 4)
												{
													text3 += "ｽﾄ";
												}
												else if ((selectedIndex49 >= 5 && selectedIndex49 <= 10) || (selectedIndex49 >= 12 && selectedIndex49 <= 17))
												{
													text3 += "ﾝﾃ";
												}
												else if (selectedIndex49 == 11)
												{
													text3 += "＜";
												}
											}
											else if (decimal.Compare(d, 62654m) == 0)
											{
												int selectedIndex50 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex50 >= 2 && selectedIndex50 <= 4)
												{
													text3 += "ﾛﾑ";
												}
												else if ((selectedIndex50 >= 5 && selectedIndex50 <= 10) || (selectedIndex50 >= 12 && selectedIndex50 <= 17))
												{
													text3 += "ﾞｽ";
												}
												else if (selectedIndex50 == 11)
												{
													text3 += "＞";
												}
											}
											else if (decimal.Compare(d, 62655m) == 0)
											{
												int selectedIndex51 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex51 == 2)
												{
													text3 += "\u3000";
												}
												else if (selectedIndex51 >= 3 && selectedIndex51 <= 17)
												{
													text3 += "條";
												}
											}
											else if (decimal.Compare(d, 62727m) == 0)
											{
												int selectedIndex52 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex52 >= 2 && selectedIndex52 <= 12)
												{
													text3 += "\u3000";
												}
												else if (selectedIndex52 >= 13 && selectedIndex52 <= 17)
												{
													text3 += "TI";
												}
											}
											else if (decimal.Compare(d, 62728m) == 0)
											{
												int selectedIndex53 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex53 >= 2 && selectedIndex53 <= 12)
												{
													text3 += "\u3000";
												}
												else if (selectedIndex53 >= 13 && selectedIndex53 <= 17)
												{
													text3 += "SM";
												}
											}
											else if (decimal.Compare(d, 62729m) == 0)
											{
												int selectedIndex54 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex54 >= 2 && selectedIndex54 <= 12)
												{
													text3 += "\u3000";
												}
												else if (selectedIndex54 >= 13 && selectedIndex54 <= 17)
												{
													text3 += "AN";
												}
											}
											else if (decimal.Compare(d, 62730m) == 0)
											{
												int selectedIndex55 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex55 >= 2 && selectedIndex55 <= 12)
												{
													text3 += "\u3000";
												}
												else if (selectedIndex55 >= 13 && selectedIndex55 <= 17)
												{
													text3 += "SA";
												}
											}
											else if (decimal.Compare(d, 62731m) == 0)
											{
												int selectedIndex56 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex56 >= 2 && selectedIndex56 <= 12)
												{
													text3 += "\u3000";
												}
												else if (selectedIndex56 >= 13 && selectedIndex56 <= 17)
												{
													text3 += "SL";
												}
											}
											else if (decimal.Compare(d, 62736m) == 0)
											{
												int selectedIndex57 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex57 >= 2 && selectedIndex57 <= 12)
												{
													text3 += "\u3000";
												}
												else if (selectedIndex57 >= 13 && selectedIndex57 <= 17)
												{
													text3 += "ﾛ!";
												}
											}
											else if (decimal.Compare(d, 62737m) == 0)
											{
												int selectedIndex58 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex58 >= 2 && selectedIndex58 <= 12)
												{
													text3 += "\u3000";
												}
												else if (selectedIndex58 >= 13 && selectedIndex58 <= 17)
												{
													text3 += "ﾛ?";
												}
											}
											else if (decimal.Compare(d, 59392m) >= 0 && decimal.Compare(d, 63393m) <= 0)
											{
												text3 += Strings.Mid(array4[Convert.ToInt32(decimal.Subtract(new decimal(array[(int)num2]), 230m))], Convert.ToInt32(decimal.Add(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))]), 1m)), 1);
												decimal d2 = decimal.Add(decimal.Multiply(new decimal(array[(int)num2]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))]));
												if (decimal.Compare(d2, 63278m) == 0)
												{
													text3 += "ﾞ";
												}
												else if (decimal.Compare(d2, 63288m) >= 0 && decimal.Compare(d2, 63307m) <= 0)
												{
													text3 += "ﾞ";
												}
												else if (decimal.Compare(d2, 63308m) >= 0 && decimal.Compare(d2, 63312m) <= 0)
												{
													text3 += "ﾟ";
												}
											}
											else
											{
												text3 += "\u3000";
											}
											b2 = 0;
											b5 = 1;
											num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
										}
										else
										{
											ulong num11 = num2;
											if (num11 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
										}
									}
									else
									{
										switch (num10)
										{
										case 248uL:
										{
											decimal d3 = decimal.Add(decimal.Multiply(new decimal(array[(int)num2]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))]));
											byte b6;
											if (decimal.Compare(d3, 63488m) == 0)
											{
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													text3 += "▼";
													b2 = 0;
													b5 = 1;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													break;
												}
												ulong num35 = num2;
												if (num35 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												break;
											}
											if (decimal.Compare(d3, 63489m) == 0)
											{
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													text3 += "▼[消去]";
													b2 = 0;
													b5 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num36 = num2;
													if (num36 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63490m) == 0)
											{
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[イベ強制終了]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num37 = num2;
													if (num37 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63491m) == 0)
											{
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[文速]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num38 = num2;
													if (num38 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63492m) == 0)
											{
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[文戻]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num39 = num2;
													if (num39 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63493m) == 0)
											{
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[文遅]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num40 = num2;
													if (num40 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63494m) == 0)
											{
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[文最遅]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num41 = num2;
													if (num41 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63495m) == 0)
											{
												b6 = 4;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))])));
													text3 = text3 + "[音0x" + $"{array2[1]:X4}" + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
													break;
												}
												ulong num42 = num2;
												if (num42 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num42 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num42 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
												break;
											}
											if (decimal.Compare(d3, 63496m) == 0)
											{
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													text3 += "[強調]【";
													b2 = 0;
													b5 = 1;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													break;
												}
												ulong num43 = num2;
												if (num43 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												break;
											}
											if (decimal.Compare(d3, 63497m) == 0)
											{
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													text3 += "】";
													b2 = 0;
													b5 = 1;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													break;
												}
												ulong num44 = num2;
												if (num44 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												break;
											}
											if (decimal.Compare(d3, 63498m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													text3 = text3 + "[2Byte数値表示," + Conversions.ToString(array2[1]) + "番目]";
													b2 = 0;
													b5 = 1;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													break;
												}
												ulong num45 = num2;
												if (num45 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num45 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												break;
											}
											if (decimal.Compare(d3, 63499m) == 0)
											{
												int selectedIndex62 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex62 >= 2 && selectedIndex62 <= 7)
												{
													b6 = 3;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														text3 = text3 + "[小背景0x" + $"{array2[1]:X2}" + "]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num46 = num2;
														if (num46 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num46 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
													}
												}
												else
												{
													if (selectedIndex62 != 8 && selectedIndex62 != 9 && selectedIndex62 != 10 && (selectedIndex62 < 11 || selectedIndex62 > 17))
													{
														break;
													}
													b6 = 4;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))])));
														text3 = text3 + "[小背景0x" + $"{array2[1]:X4}" + "]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													ulong num47 = num2;
													if (num47 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num47 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num47 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63500m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													text3 = text3 + "[左絵0x" + $"{array2[1]:X2}" + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num48 = num2;
													if (num48 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num48 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63501m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													text3 = text3 + "[右絵0x" + $"{array2[1]:X2}" + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num49 = num2;
													if (num49 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num49 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63502m) == 0)
											{
												b6 = 5;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))])));
													text3 = text3 + "[数値代入," + Conversions.ToString(array2[1]) + "番目=" + Conversions.ToString(array2[2]) + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
													break;
												}
												ulong num50 = num2;
												if (num50 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num50 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num50 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
												else if (num50 == (ulong)(b3 - 3))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													num2 = b3;
													b2 = 4;
												}
												break;
											}
											if (decimal.Compare(d3, 63503m) == 0)
											{
												b6 = 5;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))])));
													text3 = text3 + "[数値加算," + Conversions.ToString(array2[1]) + "番目+" + Conversions.ToString(array2[2]) + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
													break;
												}
												ulong num51 = num2;
												if (num51 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num51 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num51 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
												else if (num51 == (ulong)(b3 - 3))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													num2 = b3;
													b2 = 4;
												}
												break;
											}
											if (decimal.Compare(d3, 63504m) == 0)
											{
												b6 = 5;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))])));
													text3 = text3 + "[数値減算," + Conversions.ToString(array2[1]) + "番目-" + Conversions.ToString(array2[2]) + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
													break;
												}
												ulong num52 = num2;
												if (num52 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num52 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num52 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
												else if (num52 == (ulong)(b3 - 3))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													num2 = b3;
													b2 = 4;
												}
												break;
											}
											if (decimal.Compare(d3, 63505m) == 0)
											{
												b6 = 5;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))])));
													text3 = text3 + "[GBA乱数1," + Conversions.ToString(array2[1]) + "番目=0～" + Conversions.ToString(array2[2]) + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
													break;
												}
												ulong num53 = num2;
												if (num53 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num53 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num53 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
												else if (num53 == (ulong)(b3 - 3))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													num2 = b3;
													b2 = 4;
												}
												break;
											}
											if (decimal.Compare(d3, 63506m) == 0)
											{
												b6 = 5;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))])));
													text3 = text3 + "[GBA乱数2," + Conversions.ToString(array2[1]) + "番目=0～" + Conversions.ToString(array2[2]) + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
													break;
												}
												ulong num54 = num2;
												if (num54 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num54 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num54 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
												else if (num54 == (ulong)(b3 - 3))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													num2 = b3;
													b2 = 4;
												}
												break;
											}
											if (decimal.Compare(d3, 63507m) == 0)
											{
												b6 = 4;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													text3 = text3 + "[アドレス数値代入1," + Conversions.ToString(array2[1]) + "番目=" + Conversions.ToString(array2[2]) + "番目]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num55 = num2;
													if (num55 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num55 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num55 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63508m) == 0)
											{
												b6 = 5;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))])));
													text3 = text3 + "[フラグ書込," + Conversions.ToString(array2[1]) + "番目,0x" + $"{array2[2]:X4}" + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
													break;
												}
												ulong num56 = num2;
												if (num56 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num56 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num56 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
												else if (num56 == (ulong)(b3 - 3))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													num2 = b3;
													b2 = 4;
												}
												break;
											}
											if (decimal.Compare(d3, 63509m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 = ((decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 1m) != 0) ? (text3 + "[選択肢1," + Conversions.ToString(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]) + "択]") : (text3 + "[選択肢1,Yes/No]"));
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
													break;
												}
												ulong num57 = num2;
												if (num57 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num57 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												break;
											}
											if (decimal.Compare(d3, 63510m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 = ((decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 1m) != 0) ? (text3 + "[選択肢2," + Conversions.ToString(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]) + "択]") : (text3 + "[選択肢2,Yes/No]"));
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
													break;
												}
												ulong num58 = num2;
												if (num58 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num58 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												break;
											}
											if (decimal.Compare(d3, 63511m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													text3 = text3 + "[Case分岐," + Conversions.ToString(array2[1]) + "番目]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num59 = num2;
													if (num59 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num59 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63512m) == 0)
											{
												int selectedIndex63 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex63 >= 2 && selectedIndex63 <= 12)
												{
													b6 = 3;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														if (decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 24m) == 0)
														{
															text3 += "[Case0]【";
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
														}
														else
														{
															text3 += "[F818]";
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														}
														b2 = 0;
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num60 = num2;
														if (num60 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num60 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
													}
												}
												else
												{
													if (selectedIndex63 < 13 || selectedIndex63 > 17)
													{
														break;
													}
													b6 = 3;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														text3 = text3 + "[Case" + Conversions.ToString(array2[1]) + "]【";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num61 = num2;
														if (num61 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num61 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63513m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													if (decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 25m) == 0)
													{
														text3 += "[Case1]【";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													}
													else
													{
														text3 += "[F819]";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													}
													b2 = 0;
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num62 = num2;
													if (num62 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num62 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63514m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													if (decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 26m) == 0)
													{
														text3 += "[Case2]【";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													}
													else
													{
														text3 += "[F81A]";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													}
													b2 = 0;
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num63 = num2;
													if (num63 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num63 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63515m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													if (decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 27m) == 0)
													{
														text3 += "[Case3]【";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													}
													else
													{
														text3 += "[F81B]";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													}
													b2 = 0;
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num64 = num2;
													if (num64 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num64 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63516m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													if (decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 28m) == 0)
													{
														text3 += "[Case4]【";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													}
													else
													{
														text3 += "[F81C]";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													}
													b2 = 0;
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num65 = num2;
													if (num65 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num65 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63517m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													if (decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 29m) == 0)
													{
														text3 += "[Case5]【";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													}
													else
													{
														text3 += "[F81D]";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													}
													b2 = 0;
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num66 = num2;
													if (num66 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num66 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63518m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													if (decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 30m) == 0)
													{
														text3 += "[Case6]【";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													}
													else
													{
														text3 += "[F81E]";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													}
													b2 = 0;
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num67 = num2;
													if (num67 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num67 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63519m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													if (decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 31m) == 0)
													{
														text3 += "[Case7]【";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													}
													else
													{
														text3 += "[F81F]";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													}
													b2 = 0;
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num68 = num2;
													if (num68 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num68 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63520m) == 0)
											{
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "】";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num69 = num2;
													if (num69 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63521m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													if (decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 33m) == 0)
													{
														text3 += "[Case分岐終了]";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													}
													else
													{
														text3 += "[F821]";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													}
													b2 = 0;
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num70 = num2;
													if (num70 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num70 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63522m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													text3 = text3 + "[汎用イベ呼出," + Conversions.ToString(array2[1]) + "番目]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num71 = num2;
													if (num71 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num71 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63523m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													text3 = text3 + "[イベ呼出," + Conversions.ToString(array2[1]) + "番目]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num72 = num2;
													if (num72 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num72 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63524m) == 0)
											{
												int selectedIndex64 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex64 >= 2 && selectedIndex64 <= 6)
												{
													b6 = 5;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))])));
														text3 = text3 + "[イベ呼出分岐," + Conversions.ToString(array2[1]) + "番目,以後" + Conversions.ToString(array2[2] + 1) + "バイト先まで分岐先アドレスの番目]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													ulong num73 = num2;
													if (num73 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num73 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num73 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
													else if (num73 == (ulong)(b3 - 3))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														num2 = b3;
														b2 = 4;
													}
													break;
												}
												if (selectedIndex64 == 9 || (selectedIndex64 >= 12 && selectedIndex64 <= 17))
												{
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														text3 += "[オリ変名]";
														b2 = 0;
														b5 = 1;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														break;
													}
													ulong num74 = num2;
													if (num74 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													break;
												}
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[F824]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num75 = num2;
													if (num75 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63525m) == 0)
											{
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													text3 += "【名前】";
													b2 = 0;
													b5 = 1;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													break;
												}
												ulong num76 = num2;
												if (num76 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												break;
											}
											if (decimal.Compare(d3, 63526m) == 0)
											{
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													text3 += "【メインポジション】";
													b2 = 0;
													b5 = 1;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													break;
												}
												ulong num77 = num2;
												if (num77 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												break;
											}
											if (decimal.Compare(d3, 63527m) == 0)
											{
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[F827]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num78 = num2;
													if (num78 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63528m) == 0)
											{
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													int selectedIndex65 = 文字コード選択ComboBox.SelectedIndex;
													text3 = ((selectedIndex65 != 8 && selectedIndex65 != 11) ? (text3 + "【所属球団】") : (text3 + "【人物名】"));
													b2 = 0;
													b5 = 1;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													break;
												}
												ulong num79 = num2;
												if (num79 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												break;
											}
											if (decimal.Compare(d3, 63529m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													text3 = text3 + "[ディレイ" + Conversions.ToString(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]) + "(F)]";
													b2 = 0;
													b5 = 1;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													break;
												}
												ulong num80 = num2;
												if (num80 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num80 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												break;
											}
											if (decimal.Compare(d3, 63530m) == 0)
											{
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[F82A]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num81 = num2;
													if (num81 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63531m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													text3 = text3 + "[スプリクト呼出1," + Conversions.ToString(array2[1]) + "番目]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num82 = num2;
													if (num82 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num82 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63532m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													text3 = text3 + "[スプリクト呼出2," + Conversions.ToString(array2[1]) + "番目]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num83 = num2;
													if (num83 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num83 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63533m) == 0)
											{
												b6 = 8;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
													{
													case 1uL:
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
														int selectedIndex67 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex67 >= 2 && selectedIndex67 <= 12)
														{
															text3 = text3 + "[●フラグIf分岐," + Conversions.ToString(array2[1]) + "番目=0x" + $"{array2[2]:X4}" + "]";
														}
														else if (selectedIndex67 >= 13 && selectedIndex67 <= 17)
														{
															text3 = text3 + "[フラグIf分岐," + Conversions.ToString(array2[1]) + "番目=0x" + $"{array2[2]:X4}" + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													case 2uL:
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
														int selectedIndex68 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex68 >= 2 && selectedIndex68 <= 12)
														{
															text3 = text3 + "[●フラグIf分岐," + Conversions.ToString(array2[1]) + "番目=0x" + $"{array2[2]:X8}" + "]";
														}
														else if (selectedIndex68 >= 13 && selectedIndex68 <= 17)
														{
															text3 = text3 + "[フラグIf分岐," + Conversions.ToString(array2[1]) + "番目=0x" + $"{array2[2]:X8}" + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													default:
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														int selectedIndex66 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex66 >= 2 && selectedIndex66 <= 12)
														{
															text3 = text3 + "[●フラグIf分岐," + Conversions.ToString(array2[1]) + "番目=0x" + $"{array2[2]:X2}" + "]";
														}
														else if (selectedIndex66 >= 13 && selectedIndex66 <= 17)
														{
															text3 = text3 + "[フラグIf分岐," + Conversions.ToString(array2[1]) + "番目=0x" + $"{array2[2]:X2}" + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													}
												}
												else
												{
													ulong num84 = num2;
													if (num84 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num84 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num84 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
													else if (num84 == (ulong)(b3 - 3))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														num2 = b3;
														b2 = 4;
													}
													else if (num84 == (ulong)(b3 - 4))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														num2 = b3;
														b2 = 5;
													}
													else if (num84 == (ulong)(b3 - 5))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														num2 = b3;
														b2 = 6;
													}
													else if (num84 == (ulong)(b3 - 6))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
														num2 = b3;
														b2 = 7;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63534m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													if (decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 46m) == 0)
													{
														int selectedIndex69 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex69 >= 2 && selectedIndex69 <= 12)
														{
															text3 += "●[Else]【";
														}
														else if (selectedIndex69 >= 13 && selectedIndex69 <= 17)
														{
															text3 += "[Else]【";
														}
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													}
													else
													{
														text3 += "[F82E]";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													}
													b2 = 0;
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num85 = num2;
													if (num85 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num85 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63535m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													if (decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 47m) == 0)
													{
														int selectedIndex70 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex70 >= 2 && selectedIndex70 <= 12)
														{
															text3 += "】●";
														}
														else if (selectedIndex70 >= 13 && selectedIndex70 <= 17)
														{
															text3 += "】";
														}
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													}
													else
													{
														text3 += "[F82F]";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													}
													b2 = 0;
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num86 = num2;
													if (num86 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num86 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63536m) == 0)
											{
												b6 = 8;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
													{
													case 1uL:
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
														int selectedIndex72 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex72 >= 2 && selectedIndex72 <= 12)
														{
															text3 = text3 + "[●If分岐," + Conversions.ToString(array2[1]) + "番目=" + Conversions.ToString(array2[2]) + "]";
														}
														else if (selectedIndex72 >= 13 && selectedIndex72 <= 17)
														{
															text3 = text3 + "[If分岐," + Conversions.ToString(array2[1]) + "番目=" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													case 2uL:
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
														int selectedIndex73 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex73 >= 2 && selectedIndex73 <= 12)
														{
															text3 = text3 + "[●If分岐," + Conversions.ToString(array2[1]) + "番目=" + Conversions.ToString(array2[2]) + "]";
														}
														else if (selectedIndex73 >= 13 && selectedIndex73 <= 17)
														{
															text3 = text3 + "[If分岐," + Conversions.ToString(array2[1]) + "番目=" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													default:
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														int selectedIndex71 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex71 >= 2 && selectedIndex71 <= 12)
														{
															text3 = text3 + "[●If分岐," + Conversions.ToString(array2[1]) + "番目=" + Conversions.ToString(array2[2]) + "]";
														}
														else if (selectedIndex71 >= 13 && selectedIndex71 <= 17)
														{
															text3 = text3 + "[If分岐," + Conversions.ToString(array2[1]) + "番目=" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													}
												}
												else
												{
													ulong num87 = num2;
													if (num87 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num87 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num87 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
													else if (num87 == (ulong)(b3 - 3))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														num2 = b3;
														b2 = 4;
													}
													else if (num87 == (ulong)(b3 - 4))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														num2 = b3;
														b2 = 5;
													}
													else if (num87 == (ulong)(b3 - 5))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														num2 = b3;
														b2 = 6;
													}
													else if (num87 == (ulong)(b3 - 6))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
														num2 = b3;
														b2 = 7;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63537m) == 0)
											{
												b6 = 8;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
													{
													case 1uL:
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
														int selectedIndex75 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex75 >= 2 && selectedIndex75 <= 12)
														{
															text3 = text3 + "[●If分岐," + Conversions.ToString(array2[1]) + "番目<>" + Conversions.ToString(array2[2]) + "]";
														}
														else if (selectedIndex75 >= 13 && selectedIndex75 <= 17)
														{
															text3 = text3 + "[If分岐," + Conversions.ToString(array2[1]) + "番目<>" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													case 2uL:
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
														int selectedIndex76 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex76 >= 2 && selectedIndex76 <= 12)
														{
															text3 = text3 + "[●If分岐," + Conversions.ToString(array2[1]) + "番目<>" + Conversions.ToString(array2[2]) + "]";
														}
														else if (selectedIndex76 >= 13 && selectedIndex76 <= 17)
														{
															text3 = text3 + "[If分岐," + Conversions.ToString(array2[1]) + "番目<>" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													default:
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														int selectedIndex74 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex74 >= 2 && selectedIndex74 <= 12)
														{
															text3 = text3 + "[●If分岐," + Conversions.ToString(array2[1]) + "番目<>" + Conversions.ToString(array2[2]) + "]";
														}
														else if (selectedIndex74 >= 13 && selectedIndex74 <= 17)
														{
															text3 = text3 + "[If分岐," + Conversions.ToString(array2[1]) + "番目<>" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													}
												}
												else
												{
													ulong num88 = num2;
													if (num88 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num88 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num88 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
													else if (num88 == (ulong)(b3 - 3))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														num2 = b3;
														b2 = 4;
													}
													else if (num88 == (ulong)(b3 - 4))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														num2 = b3;
														b2 = 5;
													}
													else if (num88 == (ulong)(b3 - 5))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														num2 = b3;
														b2 = 6;
													}
													else if (num88 == (ulong)(b3 - 6))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
														num2 = b3;
														b2 = 7;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63538m) == 0)
											{
												b6 = 8;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
													{
													case 1uL:
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
														int selectedIndex78 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex78 >= 2 && selectedIndex78 <= 12)
														{
															text3 = text3 + "[●If分岐," + Conversions.ToString(array2[1]) + "番目>" + Conversions.ToString(array2[2]) + "]";
														}
														else if (selectedIndex78 >= 13 && selectedIndex78 <= 17)
														{
															text3 = text3 + "[If分岐," + Conversions.ToString(array2[1]) + "番目>" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													case 2uL:
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
														int selectedIndex79 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex79 >= 2 && selectedIndex79 <= 12)
														{
															text3 = text3 + "[●If分岐," + Conversions.ToString(array2[1]) + "番目>" + Conversions.ToString(array2[2]) + "]";
														}
														else if (selectedIndex79 >= 13 && selectedIndex79 <= 17)
														{
															text3 = text3 + "[If分岐," + Conversions.ToString(array2[1]) + "番目>" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													default:
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														int selectedIndex77 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex77 >= 2 && selectedIndex77 <= 12)
														{
															text3 = text3 + "[●If分岐," + Conversions.ToString(array2[1]) + "番目>" + Conversions.ToString(array2[2]) + "]";
														}
														else if (selectedIndex77 >= 13 && selectedIndex77 <= 17)
														{
															text3 = text3 + "[If分岐," + Conversions.ToString(array2[1]) + "番目>" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													}
												}
												else
												{
													ulong num89 = num2;
													if (num89 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num89 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num89 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
													else if (num89 == (ulong)(b3 - 3))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														num2 = b3;
														b2 = 4;
													}
													else if (num89 == (ulong)(b3 - 4))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														num2 = b3;
														b2 = 5;
													}
													else if (num89 == (ulong)(b3 - 5))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														num2 = b3;
														b2 = 6;
													}
													else if (num89 == (ulong)(b3 - 6))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
														num2 = b3;
														b2 = 7;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63539m) == 0)
											{
												b6 = 8;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
													{
													case 1uL:
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
														int selectedIndex81 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex81 >= 2 && selectedIndex81 <= 12)
														{
															text3 = text3 + "[●If分岐," + Conversions.ToString(array2[1]) + "番目>=" + Conversions.ToString(array2[2]) + "]";
														}
														else if (selectedIndex81 >= 13 && selectedIndex81 <= 17)
														{
															text3 = text3 + "[If分岐," + Conversions.ToString(array2[1]) + "番目>=" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													case 2uL:
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
														int selectedIndex82 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex82 >= 2 && selectedIndex82 <= 12)
														{
															text3 = text3 + "[●If分岐," + Conversions.ToString(array2[1]) + "番目>=" + Conversions.ToString(array2[2]) + "]";
														}
														else if (selectedIndex82 >= 13 && selectedIndex82 <= 17)
														{
															text3 = text3 + "[If分岐," + Conversions.ToString(array2[1]) + "番目>=" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													default:
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														int selectedIndex80 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex80 >= 2 && selectedIndex80 <= 12)
														{
															text3 = text3 + "[●If分岐," + Conversions.ToString(array2[1]) + "番目>=" + Conversions.ToString(array2[2]) + "]";
														}
														else if (selectedIndex80 >= 13 && selectedIndex80 <= 17)
														{
															text3 = text3 + "[If分岐," + Conversions.ToString(array2[1]) + "番目>=" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													}
												}
												else
												{
													ulong num90 = num2;
													if (num90 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num90 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num90 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
													else if (num90 == (ulong)(b3 - 3))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														num2 = b3;
														b2 = 4;
													}
													else if (num90 == (ulong)(b3 - 4))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														num2 = b3;
														b2 = 5;
													}
													else if (num90 == (ulong)(b3 - 5))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														num2 = b3;
														b2 = 6;
													}
													else if (num90 == (ulong)(b3 - 6))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
														num2 = b3;
														b2 = 7;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63540m) == 0)
											{
												b6 = 8;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
													{
													case 1uL:
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
														int selectedIndex84 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex84 >= 2 && selectedIndex84 <= 12)
														{
															text3 = text3 + "[●If分岐," + Conversions.ToString(array2[1]) + "番目<" + Conversions.ToString(array2[2]) + "]";
														}
														else if (selectedIndex84 >= 13 && selectedIndex84 <= 17)
														{
															text3 = text3 + "[If分岐," + Conversions.ToString(array2[1]) + "番目<" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													case 2uL:
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
														int selectedIndex85 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex85 >= 2 && selectedIndex85 <= 12)
														{
															text3 = text3 + "[●If分岐," + Conversions.ToString(array2[1]) + "番目<" + Conversions.ToString(array2[2]) + "]";
														}
														else if (selectedIndex85 >= 13 && selectedIndex85 <= 17)
														{
															text3 = text3 + "[If分岐," + Conversions.ToString(array2[1]) + "番目<" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													default:
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														int selectedIndex83 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex83 >= 2 && selectedIndex83 <= 12)
														{
															text3 = text3 + "[●If分岐," + Conversions.ToString(array2[1]) + "番目<" + Conversions.ToString(array2[2]) + "]";
														}
														else if (selectedIndex83 >= 13 && selectedIndex83 <= 17)
														{
															text3 = text3 + "[If分岐," + Conversions.ToString(array2[1]) + "番目<" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													}
												}
												else
												{
													ulong num91 = num2;
													if (num91 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num91 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num91 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
													else if (num91 == (ulong)(b3 - 3))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														num2 = b3;
														b2 = 4;
													}
													else if (num91 == (ulong)(b3 - 4))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														num2 = b3;
														b2 = 5;
													}
													else if (num91 == (ulong)(b3 - 5))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														num2 = b3;
														b2 = 6;
													}
													else if (num91 == (ulong)(b3 - 6))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
														num2 = b3;
														b2 = 7;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63541m) == 0)
											{
												b6 = 8;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
													{
													case 1uL:
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
														int selectedIndex87 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex87 >= 2 && selectedIndex87 <= 12)
														{
															text3 = text3 + "[●If分岐," + Conversions.ToString(array2[1]) + "番目<=" + Conversions.ToString(array2[2]) + "]";
														}
														else if (selectedIndex87 >= 13 && selectedIndex87 <= 17)
														{
															text3 = text3 + "[If分岐," + Conversions.ToString(array2[1]) + "番目<=" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													case 2uL:
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
														int selectedIndex88 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex88 >= 2 && selectedIndex88 <= 12)
														{
															text3 = text3 + "[●If分岐," + Conversions.ToString(array2[1]) + "番目<=" + Conversions.ToString(array2[2]) + "]";
														}
														else if (selectedIndex88 >= 13 && selectedIndex88 <= 17)
														{
															text3 = text3 + "[If分岐," + Conversions.ToString(array2[1]) + "番目<=" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													default:
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														int selectedIndex86 = 文字コード選択ComboBox.SelectedIndex;
														if (selectedIndex86 >= 2 && selectedIndex86 <= 12)
														{
															text3 = text3 + "[●If分岐," + Conversions.ToString(array2[1]) + "番目<=" + Conversions.ToString(array2[2]) + "]";
														}
														else if (selectedIndex86 >= 13 && selectedIndex86 <= 17)
														{
															text3 = text3 + "[If分岐," + Conversions.ToString(array2[1]) + "番目<=" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													}
												}
												else
												{
													ulong num92 = num2;
													if (num92 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num92 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num92 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
													else if (num92 == (ulong)(b3 - 3))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														num2 = b3;
														b2 = 4;
													}
													else if (num92 == (ulong)(b3 - 4))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														num2 = b3;
														b2 = 5;
													}
													else if (num92 == (ulong)(b3 - 5))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														num2 = b3;
														b2 = 6;
													}
													else if (num92 == (ulong)(b3 - 6))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
														num2 = b3;
														b2 = 7;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63542m) == 0)
											{
												int selectedIndex89 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex89 >= 2 && selectedIndex89 <= 12)
												{
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
														{
														case 1uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
															text3 = text3 + "[▲フラグIf分岐," + Conversions.ToString(array2[1]) + "番目=0x" + $"{array2[2]:X4}" + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														case 2uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
															text3 = text3 + "[▲フラグIf分岐," + Conversions.ToString(array2[1]) + "番目=0x" + $"{array2[2]:X8}" + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														default:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															text3 = text3 + "[▲フラグIf分岐," + Conversions.ToString(array2[1]) + "番目=0x" + $"{array2[2]:X2}" + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														}
													}
													else
													{
														ulong num93 = num2;
														if (num93 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num93 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num93 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
														else if (num93 == (ulong)(b3 - 3))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															num2 = b3;
															b2 = 4;
														}
														else if (num93 == (ulong)(b3 - 4))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															num2 = b3;
															b2 = 5;
														}
														else if (num93 == (ulong)(b3 - 5))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															num2 = b3;
															b2 = 6;
														}
														else if (num93 == (ulong)(b3 - 6))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
															num2 = b3;
															b2 = 7;
														}
													}
												}
												else
												{
													if (selectedIndex89 < 13 || selectedIndex89 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F836]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num94 = num2;
														if (num94 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63543m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													if ((decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 55m) == 0) & (文字コード選択ComboBox.SelectedIndex <= 12))
													{
														text3 += "▲[Else]【";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													}
													else
													{
														text3 += "[F837]";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													}
													b2 = 0;
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num95 = num2;
													if (num95 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num95 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63544m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													if ((decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 56m) == 0) & (文字コード選択ComboBox.SelectedIndex <= 12))
													{
														text3 += "】▲";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													}
													else
													{
														text3 += "[F838]";
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													}
													b2 = 0;
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num96 = num2;
													if (num96 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num96 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63545m) == 0)
											{
												int selectedIndex90 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex90 >= 2 && selectedIndex90 <= 12)
												{
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
														{
														case 1uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
															text3 = text3 + "[▲If分岐," + Conversions.ToString(array2[1]) + "番目=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														case 2uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
															text3 = text3 + "[▲If分岐," + Conversions.ToString(array2[1]) + "番目=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														default:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															text3 = text3 + "[▲If分岐," + Conversions.ToString(array2[1]) + "番目=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														}
													}
													else
													{
														ulong num97 = num2;
														if (num97 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num97 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num97 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
														else if (num97 == (ulong)(b3 - 3))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															num2 = b3;
															b2 = 4;
														}
														else if (num97 == (ulong)(b3 - 4))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															num2 = b3;
															b2 = 5;
														}
														else if (num97 == (ulong)(b3 - 5))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															num2 = b3;
															b2 = 6;
														}
														else if (num97 == (ulong)(b3 - 6))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
															num2 = b3;
															b2 = 7;
														}
													}
												}
												else
												{
													if (selectedIndex90 < 13 || selectedIndex90 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F839]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num98 = num2;
														if (num98 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63546m) == 0)
											{
												int selectedIndex91 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex91 >= 2 && selectedIndex91 <= 12)
												{
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
														{
														case 1uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
															text3 = text3 + "[▲If分岐," + Conversions.ToString(array2[1]) + "番目<>" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														case 2uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
															text3 = text3 + "[▲If分岐," + Conversions.ToString(array2[1]) + "番目<>" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														default:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															text3 = text3 + "[▲If分岐," + Conversions.ToString(array2[1]) + "番目<>" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														}
													}
													else
													{
														ulong num99 = num2;
														if (num99 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num99 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num99 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
														else if (num99 == (ulong)(b3 - 3))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															num2 = b3;
															b2 = 4;
														}
														else if (num99 == (ulong)(b3 - 4))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															num2 = b3;
															b2 = 5;
														}
														else if (num99 == (ulong)(b3 - 5))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															num2 = b3;
															b2 = 6;
														}
														else if (num99 == (ulong)(b3 - 6))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
															num2 = b3;
															b2 = 7;
														}
													}
												}
												else
												{
													if (selectedIndex91 < 13 || selectedIndex91 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F83A]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num100 = num2;
														if (num100 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63547m) == 0)
											{
												int selectedIndex92 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex92 >= 2 && selectedIndex92 <= 12)
												{
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
														{
														case 1uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
															text3 = text3 + "[▲If分岐," + Conversions.ToString(array2[1]) + "番目>" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														case 2uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
															text3 = text3 + "[▲If分岐," + Conversions.ToString(array2[1]) + "番目>" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														default:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															text3 = text3 + "[▲If分岐," + Conversions.ToString(array2[1]) + "番目>" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														}
													}
													else
													{
														ulong num101 = num2;
														if (num101 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num101 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num101 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
														else if (num101 == (ulong)(b3 - 3))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															num2 = b3;
															b2 = 4;
														}
														else if (num101 == (ulong)(b3 - 4))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															num2 = b3;
															b2 = 5;
														}
														else if (num101 == (ulong)(b3 - 5))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															num2 = b3;
															b2 = 6;
														}
														else if (num101 == (ulong)(b3 - 6))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
															num2 = b3;
															b2 = 7;
														}
													}
												}
												else
												{
													if (selectedIndex92 < 13 || selectedIndex92 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F83B]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num102 = num2;
														if (num102 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63548m) == 0)
											{
												int selectedIndex93 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex93 >= 2 && selectedIndex93 <= 12)
												{
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
														{
														case 1uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
															text3 = text3 + "[▲If分岐," + Conversions.ToString(array2[1]) + "番目>=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														case 2uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
															text3 = text3 + "[▲If分岐," + Conversions.ToString(array2[1]) + "番目>=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														default:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															text3 = text3 + "[▲If分岐," + Conversions.ToString(array2[1]) + "番目>=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														}
													}
													else
													{
														ulong num103 = num2;
														if (num103 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num103 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num103 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
														else if (num103 == (ulong)(b3 - 3))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															num2 = b3;
															b2 = 4;
														}
														else if (num103 == (ulong)(b3 - 4))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															num2 = b3;
															b2 = 5;
														}
														else if (num103 == (ulong)(b3 - 5))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															num2 = b3;
															b2 = 6;
														}
														else if (num103 == (ulong)(b3 - 6))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
															num2 = b3;
															b2 = 7;
														}
													}
												}
												else
												{
													if (selectedIndex93 < 13 || selectedIndex93 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F83C]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num104 = num2;
														if (num104 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63549m) == 0)
											{
												int selectedIndex94 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex94 >= 2 && selectedIndex94 <= 12)
												{
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
														{
														case 1uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
															text3 = text3 + "[▲If分岐," + Conversions.ToString(array2[1]) + "番目<" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														case 2uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
															text3 = text3 + "[▲If分岐," + Conversions.ToString(array2[1]) + "番目<" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														default:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															text3 = text3 + "[▲If分岐," + Conversions.ToString(array2[1]) + "番目<" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														}
													}
													else
													{
														ulong num105 = num2;
														if (num105 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num105 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num105 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
														else if (num105 == (ulong)(b3 - 3))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															num2 = b3;
															b2 = 4;
														}
														else if (num105 == (ulong)(b3 - 4))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															num2 = b3;
															b2 = 5;
														}
														else if (num105 == (ulong)(b3 - 5))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															num2 = b3;
															b2 = 6;
														}
														else if (num105 == (ulong)(b3 - 6))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
															num2 = b3;
															b2 = 7;
														}
													}
												}
												else
												{
													if (selectedIndex94 < 13 || selectedIndex94 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F83D]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num106 = num2;
														if (num106 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63550m) == 0)
											{
												int selectedIndex95 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex95 >= 2 && selectedIndex95 <= 12)
												{
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
														{
														case 1uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
															text3 = text3 + "[▲If分岐," + Conversions.ToString(array2[1]) + "番目<=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														case 2uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
															text3 = text3 + "[▲If分岐," + Conversions.ToString(array2[1]) + "番目<=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														default:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															text3 = text3 + "[▲If分岐," + Conversions.ToString(array2[1]) + "番目<=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														}
													}
													else
													{
														ulong num107 = num2;
														if (num107 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num107 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num107 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
														else if (num107 == (ulong)(b3 - 3))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															num2 = b3;
															b2 = 4;
														}
														else if (num107 == (ulong)(b3 - 4))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															num2 = b3;
															b2 = 5;
														}
														else if (num107 == (ulong)(b3 - 5))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															num2 = b3;
															b2 = 6;
														}
														else if (num107 == (ulong)(b3 - 6))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
															num2 = b3;
															b2 = 7;
														}
													}
												}
												else
												{
													if (selectedIndex95 < 13 || selectedIndex95 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F83E]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num108 = num2;
														if (num108 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63551m) == 0)
											{
												int selectedIndex96 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex96 >= 2 && selectedIndex96 <= 12)
												{
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
														{
														case 1uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
															text3 = text3 + "[■フラグIf分岐," + Conversions.ToString(array2[1]) + "番目=0x" + $"{array2[2]:X4}" + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														case 2uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
															text3 = text3 + "[■フラグIf分岐," + Conversions.ToString(array2[1]) + "番目=0x" + $"{array2[2]:X8}" + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														default:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															text3 = text3 + "[■フラグIf分岐," + Conversions.ToString(array2[1]) + "番目=0x" + $"{array2[2]:X2}" + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														}
													}
													else
													{
														ulong num109 = num2;
														if (num109 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num109 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num109 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
														else if (num109 == (ulong)(b3 - 3))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															num2 = b3;
															b2 = 4;
														}
														else if (num109 == (ulong)(b3 - 4))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															num2 = b3;
															b2 = 5;
														}
														else if (num109 == (ulong)(b3 - 5))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															num2 = b3;
															b2 = 6;
														}
														else if (num109 == (ulong)(b3 - 6))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
															num2 = b3;
															b2 = 7;
														}
													}
												}
												else
												{
													if (selectedIndex96 < 13 || selectedIndex96 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														text3 += "[F83F]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num110 = num2;
														if (num110 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63552m) == 0)
											{
												int selectedIndex97 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex97 >= 2 && selectedIndex97 <= 12)
												{
													b6 = 3;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														if ((decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 64m) == 0) & (文字コード選択ComboBox.SelectedIndex <= 12))
														{
															text3 += "■[Else]【";
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
														}
														else
														{
															text3 += "[F840]";
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														}
														b2 = 0;
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num111 = num2;
														if (num111 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num111 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
													}
												}
												else
												{
													if (selectedIndex97 < 13 || selectedIndex97 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F840]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num112 = num2;
														if (num112 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63553m) == 0)
											{
												int selectedIndex98 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex98 >= 2 && selectedIndex98 <= 12)
												{
													b6 = 3;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														if ((decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 65m) == 0) & (文字コード選択ComboBox.SelectedIndex <= 12))
														{
															text3 += "】■";
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
														}
														else
														{
															text3 += "[F841]";
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														}
														b2 = 0;
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num113 = num2;
														if (num113 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num113 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
													}
												}
												else
												{
													if (selectedIndex98 < 13 || selectedIndex98 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F841]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num114 = num2;
														if (num114 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63554m) == 0)
											{
												int selectedIndex99 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex99 >= 2 && selectedIndex99 <= 12)
												{
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
														{
														case 1uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
															text3 = text3 + "[■If分岐," + Conversions.ToString(array2[1]) + "番目=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														case 2uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
															text3 = text3 + "[■If分岐," + Conversions.ToString(array2[1]) + "番目=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														default:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															text3 = text3 + "[■If分岐," + Conversions.ToString(array2[1]) + "番目=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														}
													}
													else
													{
														ulong num115 = num2;
														if (num115 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num115 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num115 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
														else if (num115 == (ulong)(b3 - 3))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															num2 = b3;
															b2 = 4;
														}
														else if (num115 == (ulong)(b3 - 4))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															num2 = b3;
															b2 = 5;
														}
														else if (num115 == (ulong)(b3 - 5))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															num2 = b3;
															b2 = 6;
														}
														else if (num115 == (ulong)(b3 - 6))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
															num2 = b3;
															b2 = 7;
														}
													}
												}
												else
												{
													if (selectedIndex99 < 13 || selectedIndex99 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F842]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num116 = num2;
														if (num116 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63555m) == 0)
											{
												int selectedIndex100 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex100 >= 2 && selectedIndex100 <= 12)
												{
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
														{
														case 1uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
															text3 = text3 + "[■If分岐," + Conversions.ToString(array2[1]) + "番目<>" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														case 2uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
															text3 = text3 + "[■If分岐," + Conversions.ToString(array2[1]) + "番目<>" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														default:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															text3 = text3 + "[■If分岐," + Conversions.ToString(array2[1]) + "番目<>" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														}
													}
													else
													{
														ulong num117 = num2;
														if (num117 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num117 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num117 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
														else if (num117 == (ulong)(b3 - 3))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															num2 = b3;
															b2 = 4;
														}
														else if (num117 == (ulong)(b3 - 4))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															num2 = b3;
															b2 = 5;
														}
														else if (num117 == (ulong)(b3 - 5))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															num2 = b3;
															b2 = 6;
														}
														else if (num117 == (ulong)(b3 - 6))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
															num2 = b3;
															b2 = 7;
														}
													}
												}
												else
												{
													if (selectedIndex100 < 13 || selectedIndex100 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F843]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num118 = num2;
														if (num118 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63556m) == 0)
											{
												int selectedIndex101 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex101 >= 2 && selectedIndex101 <= 12)
												{
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
														{
														case 1uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
															text3 = text3 + "[■If分岐," + Conversions.ToString(array2[1]) + "番目>" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														case 2uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
															text3 = text3 + "[■If分岐," + Conversions.ToString(array2[1]) + "番目>" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														default:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															text3 = text3 + "[■If分岐," + Conversions.ToString(array2[1]) + "番目>" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														}
													}
													else
													{
														ulong num119 = num2;
														if (num119 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num119 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num119 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
														else if (num119 == (ulong)(b3 - 3))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															num2 = b3;
															b2 = 4;
														}
														else if (num119 == (ulong)(b3 - 4))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															num2 = b3;
															b2 = 5;
														}
														else if (num119 == (ulong)(b3 - 5))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															num2 = b3;
															b2 = 6;
														}
														else if (num119 == (ulong)(b3 - 6))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
															num2 = b3;
															b2 = 7;
														}
													}
												}
												else
												{
													if (selectedIndex101 < 13 || selectedIndex101 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F844]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num120 = num2;
														if (num120 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63557m) == 0)
											{
												int selectedIndex102 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex102 >= 2 && selectedIndex102 <= 12)
												{
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
														{
														case 1uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
															text3 = text3 + "[■If分岐," + Conversions.ToString(array2[1]) + "番目>=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														case 2uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
															text3 = text3 + "[■If分岐," + Conversions.ToString(array2[1]) + "番目>=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														default:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															text3 = text3 + "[■If分岐," + Conversions.ToString(array2[1]) + "番目>=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														}
													}
													else
													{
														ulong num121 = num2;
														if (num121 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num121 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num121 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
														else if (num121 == (ulong)(b3 - 3))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															num2 = b3;
															b2 = 4;
														}
														else if (num121 == (ulong)(b3 - 4))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															num2 = b3;
															b2 = 5;
														}
														else if (num121 == (ulong)(b3 - 5))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															num2 = b3;
															b2 = 6;
														}
														else if (num121 == (ulong)(b3 - 6))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
															num2 = b3;
															b2 = 7;
														}
													}
												}
												else
												{
													if (selectedIndex102 < 13 || selectedIndex102 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F845]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num122 = num2;
														if (num122 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63558m) == 0)
											{
												int selectedIndex103 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex103 >= 2 && selectedIndex103 <= 12)
												{
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
														{
														case 1uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
															text3 = text3 + "[■If分岐," + Conversions.ToString(array2[1]) + "番目<" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														case 2uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
															text3 = text3 + "[■If分岐," + Conversions.ToString(array2[1]) + "番目<" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														default:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															text3 = text3 + "[■If分岐," + Conversions.ToString(array2[1]) + "番目<" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														}
													}
													else
													{
														ulong num123 = num2;
														if (num123 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num123 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num123 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
														else if (num123 == (ulong)(b3 - 3))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															num2 = b3;
															b2 = 4;
														}
														else if (num123 == (ulong)(b3 - 4))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															num2 = b3;
															b2 = 5;
														}
														else if (num123 == (ulong)(b3 - 5))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															num2 = b3;
															b2 = 6;
														}
														else if (num123 == (ulong)(b3 - 6))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
															num2 = b3;
															b2 = 7;
														}
													}
												}
												else
												{
													if (selectedIndex103 < 13 || selectedIndex103 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F846]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num124 = num2;
														if (num124 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63559m) == 0)
											{
												int selectedIndex104 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex104 >= 2 && selectedIndex104 <= 12)
												{
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
														{
														case 1uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
															text3 = text3 + "[■If分岐," + Conversions.ToString(array2[1]) + "番目<=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														case 2uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
															text3 = text3 + "[■If分岐," + Conversions.ToString(array2[1]) + "番目<=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														default:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															text3 = text3 + "[■If分岐," + Conversions.ToString(array2[1]) + "番目<=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														}
													}
													else
													{
														ulong num125 = num2;
														if (num125 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num125 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num125 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
														else if (num125 == (ulong)(b3 - 3))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															num2 = b3;
															b2 = 4;
														}
														else if (num125 == (ulong)(b3 - 4))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															num2 = b3;
															b2 = 5;
														}
														else if (num125 == (ulong)(b3 - 5))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															num2 = b3;
															b2 = 6;
														}
														else if (num125 == (ulong)(b3 - 6))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
															num2 = b3;
															b2 = 7;
														}
													}
												}
												else
												{
													if (selectedIndex104 < 13 || selectedIndex104 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F847]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num126 = num2;
														if (num126 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63560m) == 0)
											{
												int selectedIndex105 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex105 >= 2 && selectedIndex105 <= 12)
												{
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
														{
														case 1uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
															text3 = text3 + "[◆フラグIf分岐," + Conversions.ToString(array2[1]) + "番目=0x" + $"{array2[2]:X4}" + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														case 2uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
															text3 = text3 + "[◆フラグIf分岐," + Conversions.ToString(array2[1]) + "番目=0x" + $"{array2[2]:X8}" + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														default:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															text3 = text3 + "[◆フラグIf分岐," + Conversions.ToString(array2[1]) + "番目=0x" + $"{array2[2]:X2}" + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														}
													}
													else
													{
														ulong num127 = num2;
														if (num127 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num127 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num127 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
														else if (num127 == (ulong)(b3 - 3))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															num2 = b3;
															b2 = 4;
														}
														else if (num127 == (ulong)(b3 - 4))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															num2 = b3;
															b2 = 5;
														}
														else if (num127 == (ulong)(b3 - 5))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															num2 = b3;
															b2 = 6;
														}
														else if (num127 == (ulong)(b3 - 6))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
															num2 = b3;
															b2 = 7;
														}
													}
												}
												else
												{
													if (selectedIndex105 < 13 || selectedIndex105 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F848]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num128 = num2;
														if (num128 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63561m) == 0)
											{
												int selectedIndex106 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex106 >= 2 && selectedIndex106 <= 12)
												{
													b6 = 3;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														if ((decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 73m) == 0) & (文字コード選択ComboBox.SelectedIndex <= 12))
														{
															text3 += "◆[Else]【";
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
														}
														else
														{
															text3 += "[F849]";
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														}
														b2 = 0;
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num129 = num2;
														if (num129 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num129 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
													}
												}
												else
												{
													if (selectedIndex106 < 13 || selectedIndex106 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F849]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num130 = num2;
														if (num130 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63562m) == 0)
											{
												int selectedIndex107 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex107 >= 2 && selectedIndex107 <= 12)
												{
													b6 = 3;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														if ((decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 74m) == 0) & (文字コード選択ComboBox.SelectedIndex <= 12))
														{
															text3 += "】◆";
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
														}
														else
														{
															text3 += "[F84A]";
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														}
														b2 = 0;
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num131 = num2;
														if (num131 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num131 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
													}
												}
												else
												{
													if (selectedIndex107 < 13 || selectedIndex107 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F84A]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num132 = num2;
														if (num132 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63563m) == 0)
											{
												int selectedIndex108 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex108 >= 2 && selectedIndex108 <= 12)
												{
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
														{
														case 1uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
															text3 = text3 + "[◆If分岐," + Conversions.ToString(array2[1]) + "番目=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														case 2uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
															text3 = text3 + "[◆If分岐," + Conversions.ToString(array2[1]) + "番目=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														default:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															text3 = text3 + "[◆If分岐," + Conversions.ToString(array2[1]) + "番目=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														}
													}
													else
													{
														ulong num133 = num2;
														if (num133 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num133 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num133 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
														else if (num133 == (ulong)(b3 - 3))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															num2 = b3;
															b2 = 4;
														}
														else if (num133 == (ulong)(b3 - 4))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															num2 = b3;
															b2 = 5;
														}
														else if (num133 == (ulong)(b3 - 5))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															num2 = b3;
															b2 = 6;
														}
														else if (num133 == (ulong)(b3 - 6))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
															num2 = b3;
															b2 = 7;
														}
													}
												}
												else
												{
													if (selectedIndex108 < 13 || selectedIndex108 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F84B]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num134 = num2;
														if (num134 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63564m) == 0)
											{
												int selectedIndex109 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex109 >= 2 && selectedIndex109 <= 12)
												{
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
														{
														case 1uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
															text3 = text3 + "[◆If分岐," + Conversions.ToString(array2[1]) + "番目<>" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														case 2uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
															text3 = text3 + "[◆If分岐," + Conversions.ToString(array2[1]) + "番目<>" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														default:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															text3 = text3 + "[◆If分岐," + Conversions.ToString(array2[1]) + "番目<>" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														}
													}
													else
													{
														ulong num135 = num2;
														if (num135 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num135 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num135 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
														else if (num135 == (ulong)(b3 - 3))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															num2 = b3;
															b2 = 4;
														}
														else if (num135 == (ulong)(b3 - 4))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															num2 = b3;
															b2 = 5;
														}
														else if (num135 == (ulong)(b3 - 5))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															num2 = b3;
															b2 = 6;
														}
														else if (num135 == (ulong)(b3 - 6))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
															num2 = b3;
															b2 = 7;
														}
													}
												}
												else
												{
													if (selectedIndex109 < 13 || selectedIndex109 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F84C]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num136 = num2;
														if (num136 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63565m) == 0)
											{
												int selectedIndex110 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex110 >= 2 && selectedIndex110 <= 12)
												{
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
														{
														case 1uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
															text3 = text3 + "[◆If分岐," + Conversions.ToString(array2[1]) + "番目>" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														case 2uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
															text3 = text3 + "[◆If分岐," + Conversions.ToString(array2[1]) + "番目>" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														default:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															text3 = text3 + "[◆If分岐," + Conversions.ToString(array2[1]) + "番目>" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														}
													}
													else
													{
														ulong num137 = num2;
														if (num137 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num137 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num137 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
														else if (num137 == (ulong)(b3 - 3))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															num2 = b3;
															b2 = 4;
														}
														else if (num137 == (ulong)(b3 - 4))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															num2 = b3;
															b2 = 5;
														}
														else if (num137 == (ulong)(b3 - 5))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															num2 = b3;
															b2 = 6;
														}
														else if (num137 == (ulong)(b3 - 6))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
															num2 = b3;
															b2 = 7;
														}
													}
												}
												else
												{
													if (selectedIndex110 < 13 || selectedIndex110 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F84D]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num138 = num2;
														if (num138 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63566m) == 0)
											{
												int selectedIndex111 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex111 >= 2 && selectedIndex111 <= 12)
												{
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
														{
														case 1uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
															text3 = text3 + "[◆If分岐," + Conversions.ToString(array2[1]) + "番目>=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														case 2uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
															text3 = text3 + "[◆If分岐," + Conversions.ToString(array2[1]) + "番目>=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														default:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															text3 = text3 + "[◆If分岐," + Conversions.ToString(array2[1]) + "番目>=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														}
													}
													else
													{
														ulong num139 = num2;
														if (num139 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num139 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num139 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
														else if (num139 == (ulong)(b3 - 3))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															num2 = b3;
															b2 = 4;
														}
														else if (num139 == (ulong)(b3 - 4))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															num2 = b3;
															b2 = 5;
														}
														else if (num139 == (ulong)(b3 - 5))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															num2 = b3;
															b2 = 6;
														}
														else if (num139 == (ulong)(b3 - 6))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
															num2 = b3;
															b2 = 7;
														}
													}
												}
												else
												{
													if (selectedIndex111 < 13 || selectedIndex111 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F84E]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num140 = num2;
														if (num140 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63567m) == 0)
											{
												int selectedIndex112 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex112 >= 2 && selectedIndex112 <= 12)
												{
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
														{
														case 1uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
															text3 = text3 + "[◆If分岐," + Conversions.ToString(array2[1]) + "番目<" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														case 2uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
															text3 = text3 + "[◆If分岐," + Conversions.ToString(array2[1]) + "番目<" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														default:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															text3 = text3 + "[◆If分岐," + Conversions.ToString(array2[1]) + "番目<" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														}
													}
													else
													{
														ulong num141 = num2;
														if (num141 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num141 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num141 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
														else if (num141 == (ulong)(b3 - 3))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															num2 = b3;
															b2 = 4;
														}
														else if (num141 == (ulong)(b3 - 4))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															num2 = b3;
															b2 = 5;
														}
														else if (num141 == (ulong)(b3 - 5))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															num2 = b3;
															b2 = 6;
														}
														else if (num141 == (ulong)(b3 - 6))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
															num2 = b3;
															b2 = 7;
														}
													}
												}
												else
												{
													if (selectedIndex112 < 13 || selectedIndex112 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														text3 += "[F84F]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num142 = num2;
														if (num142 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63568m) == 0)
											{
												int selectedIndex113 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex113 >= 2 && selectedIndex113 <= 12)
												{
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														switch (array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])
														{
														case 1uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))])));
															text3 = text3 + "[◆If分岐," + Conversions.ToString(array2[1]) + "番目<=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 5m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														case 2uL:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
															text3 = text3 + "[◆If分岐," + Conversions.ToString(array2[1]) + "番目<=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														default:
															if (unchecked(b5 == 1 && b == 0))
															{
																text3 += "\r\n";
																b5 = 0;
															}
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															text3 = text3 + "[◆If分岐," + Conversions.ToString(array2[1]) + "番目<=" + Conversions.ToString(array2[2]) + "]";
															b2 = 0;
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 4m));
															if (b == 0)
															{
																text3 += "\r\n";
															}
															break;
														}
													}
													else
													{
														ulong num143 = num2;
														if (num143 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num143 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num143 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
														else if (num143 == (ulong)(b3 - 3))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															num2 = b3;
															b2 = 4;
														}
														else if (num143 == (ulong)(b3 - 4))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															num2 = b3;
															b2 = 5;
														}
														else if (num143 == (ulong)(b3 - 5))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															num2 = b3;
															b2 = 6;
														}
														else if (num143 == (ulong)(b3 - 6))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
															array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
															array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
															num2 = b3;
															b2 = 7;
														}
													}
												}
												else
												{
													if (selectedIndex113 < 13 || selectedIndex113 > 17)
													{
														break;
													}
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														text3 += "[F850]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num144 = num2;
														if (num144 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63569m) == 0)
											{
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[能力変化精算]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num145 = num2;
													if (num145 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63570m) == 0)
											{
												b6 = 4;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													if (array2[2] >= 128)
													{
														array2[2] -= 128L;
														text3 = text3 + "[補正有能力加算,種類0x" + $"{array2[1]:X2}" + ",+1～" + Conversions.ToString(array2[2]) + "]";
													}
													else
													{
														text3 = text3 + "[補正有能力加算,種類0x" + $"{array2[1]:X2}" + ",+" + Conversions.ToString(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]) + "]";
													}
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num146 = num2;
													if (num146 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num146 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num146 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63571m) == 0)
											{
												b6 = 4;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													text3 = ((array2[2] < 128) ? (text3 + "[補正有能力減算,種類0x" + $"{array2[1]:X2}" + ",-" + Conversions.ToString(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]) + "]") : (text3 + "[補正有能力減算,種類0x" + $"{array2[1]:X2}" + ",-1～" + Conversions.ToString(array2[2]) + "]"));
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num147 = num2;
													if (num147 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num147 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num147 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63572m) == 0)
											{
												int selectedIndex114 = 文字コード選択ComboBox.SelectedIndex;
												if ((selectedIndex114 >= 2 && selectedIndex114 <= 8) || selectedIndex114 == 10 || selectedIndex114 == 11)
												{
													b6 = 4;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														if (array2[2] >= 128)
														{
															array2[2] -= 128L;
															text3 = text3 + "[補正無能力加算,種類0x" + $"{array2[1]:X2}" + ",+1～" + Conversions.ToString(array2[2]) + "]";
														}
														else
														{
															text3 = text3 + "[補正無能力加算,種類0x" + $"{array2[1]:X2}" + ",+" + Conversions.ToString(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num148 = num2;
														if (num148 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num148 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num148 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
													}
												}
												else
												{
													if (selectedIndex114 != 9 && (selectedIndex114 < 12 || selectedIndex114 > 17))
													{
														break;
													}
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))])));
														array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
														if (array2[2] >= 2147483648u)
														{
															array2[2] -= 4294967296L;
															text3 = ((array2[2] > -32768) ? (text3 + "[補正無能力変化1,種類0x" + $"{array2[1]:X4}" + "," + Conversions.ToString(array2[2]) + "]") : (text3 + "[補正無能力変化1,種類0x" + $"{array2[1]:X4}" + ",-1～" + Conversions.ToString(array2[2]) + "]"));
														}
														else if (array2[2] >= 32768)
														{
															array2[2] -= 32768L;
															text3 = text3 + "[補正無能力変化1,種類0x" + $"{array2[1]:X4}" + ",+1～" + Conversions.ToString(array2[2]) + "]";
														}
														else
														{
															text3 = text3 + "[補正無能力変化1,種類0x" + $"{array2[1]:X4}" + ",+" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													ulong num149 = num2;
													if (num149 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num149 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num149 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
													else if (num149 == (ulong)(b3 - 3))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														num2 = b3;
														b2 = 4;
													}
													else if (num149 == (ulong)(b3 - 4))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														num2 = b3;
														b2 = 5;
													}
													else if (num149 == (ulong)(b3 - 5))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														num2 = b3;
														b2 = 6;
													}
													else if (num149 == (ulong)(b3 - 6))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
														num2 = b3;
														b2 = 7;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63573m) == 0)
											{
												int selectedIndex115 = 文字コード選択ComboBox.SelectedIndex;
												if ((selectedIndex115 >= 2 && selectedIndex115 <= 8) || selectedIndex115 == 10 || selectedIndex115 == 11)
												{
													b6 = 4;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														text3 = ((array2[2] < 128) ? (text3 + "[補正無能力減算,種類0x" + $"{array2[1]:X2}" + ",-" + Conversions.ToString(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]) + "]") : (text3 + "[補正無能力減算,種類0x" + $"{array2[1]:X2}" + ",-1～" + Conversions.ToString(array2[2]) + "]"));
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num150 = num2;
														if (num150 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num150 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num150 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
													}
												}
												else
												{
													if (selectedIndex115 != 9 && (selectedIndex115 < 12 || selectedIndex115 > 17))
													{
														break;
													}
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))])));
														array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
														if (array2[2] >= 2147483648u)
														{
															array2[2] -= 4294967296L;
															text3 = ((array2[2] > -32768) ? (text3 + "[補正無能力変化2,種類0x" + $"{array2[1]:X4}" + "," + Conversions.ToString(array2[2]) + "]") : (text3 + "[補正無能力変化2,種類0x" + $"{array2[1]:X4}" + ",-1～" + Conversions.ToString(array2[2]) + "]"));
														}
														else if (array2[2] >= 32768)
														{
															array2[2] -= 32768L;
															text3 = text3 + "[補正無能力変化2,種類0x" + $"{array2[1]:X4}" + ",+1～" + Conversions.ToString(array2[2]) + "]";
														}
														else
														{
															text3 = text3 + "[補正無能力変化2,種類0x" + $"{array2[1]:X4}" + ",+" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													ulong num151 = num2;
													if (num151 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num151 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num151 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
													else if (num151 == (ulong)(b3 - 3))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														num2 = b3;
														b2 = 4;
													}
													else if (num151 == (ulong)(b3 - 4))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														num2 = b3;
														b2 = 5;
													}
													else if (num151 == (ulong)(b3 - 5))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														num2 = b3;
														b2 = 6;
													}
													else if (num151 == (ulong)(b3 - 6))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
														num2 = b3;
														b2 = 7;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63574m) == 0)
											{
												int selectedIndex116 = 文字コード選択ComboBox.SelectedIndex;
												if ((selectedIndex116 >= 2 && selectedIndex116 <= 8) || selectedIndex116 == 10 || selectedIndex116 == 11)
												{
													b6 = 7;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))])));
														text3 = text3 + "[能力加算,種類0x" + $"{array2[1]:X2}" + ",+" + Conversions.ToString(array2[2]) + "]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 6m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													ulong num152 = num2;
													if (num152 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num152 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num152 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
													else if (num152 == (ulong)(b3 - 3))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														num2 = b3;
														b2 = 4;
													}
													else if (num152 == (ulong)(b3 - 4))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														num2 = b3;
														b2 = 5;
													}
													else if (num152 == (ulong)(b3 - 5))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														num2 = b3;
														b2 = 6;
													}
												}
												else
												{
													if (selectedIndex116 != 9 && (selectedIndex116 < 12 || selectedIndex116 > 17))
													{
														break;
													}
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))])));
														array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
														if (array2[2] >= 2147483648u)
														{
															array2[2] -= 4294967296L;
															text3 = ((array2[2] > -32768) ? (text3 + "[補正有能力変化1,種類0x" + $"{array2[1]:X4}" + "," + Conversions.ToString(array2[2]) + "]") : (text3 + "[補正有能力変化1,種類0x" + $"{array2[1]:X4}" + ",-1～" + Conversions.ToString(array2[2]) + "]"));
														}
														else if (array2[2] >= 32768)
														{
															array2[2] -= 32768L;
															text3 = text3 + "[補正有能力変化1,種類0x" + $"{array2[1]:X4}" + ",+1～" + Conversions.ToString(array2[2]) + "]";
														}
														else
														{
															text3 = text3 + "[補正有能力変化1,種類0x" + $"{array2[1]:X4}" + ",+" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													ulong num153 = num2;
													if (num153 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num153 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num153 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
													else if (num153 == (ulong)(b3 - 3))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														num2 = b3;
														b2 = 4;
													}
													else if (num153 == (ulong)(b3 - 4))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														num2 = b3;
														b2 = 5;
													}
													else if (num153 == (ulong)(b3 - 5))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														num2 = b3;
														b2 = 6;
													}
													else if (num153 == (ulong)(b3 - 6))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
														num2 = b3;
														b2 = 7;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63575m) == 0)
											{
												int selectedIndex117 = 文字コード選択ComboBox.SelectedIndex;
												if ((selectedIndex117 >= 2 && selectedIndex117 <= 8) || selectedIndex117 == 10 || selectedIndex117 == 11)
												{
													b6 = 7;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))])));
														text3 = text3 + "[能力減算,種類0x" + $"{array2[1]:X2}" + ",-" + Conversions.ToString(array2[2]) + "]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 6m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													ulong num154 = num2;
													if (num154 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num154 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num154 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
													else if (num154 == (ulong)(b3 - 3))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														num2 = b3;
														b2 = 4;
													}
													else if (num154 == (ulong)(b3 - 4))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														num2 = b3;
														b2 = 5;
													}
													else if (num154 == (ulong)(b3 - 5))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														num2 = b3;
														b2 = 6;
													}
												}
												else
												{
													if (selectedIndex117 != 9 && (selectedIndex117 < 12 || selectedIndex117 > 17))
													{
														break;
													}
													b6 = 8;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))])));
														array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 7m))])));
														if (array2[2] >= 2147483648u)
														{
															array2[2] -= 4294967296L;
															text3 = ((array2[2] > -32768) ? (text3 + "[補正有能力変化2,種類0x" + $"{array2[1]:X4}" + "," + Conversions.ToString(array2[2]) + "]") : (text3 + "[補正有能力変化2,種類0x" + $"{array2[1]:X4}" + ",-1～" + Conversions.ToString(array2[2]) + "]"));
														}
														else if (array2[2] >= 32768)
														{
															array2[2] -= 32768L;
															text3 = text3 + "[補正有能力変化2,種類0x" + $"{array2[1]:X4}" + ",+1～" + Conversions.ToString(array2[2]) + "]";
														}
														else
														{
															text3 = text3 + "[補正有能力変化2,種類0x" + $"{array2[1]:X4}" + ",+" + Conversions.ToString(array2[2]) + "]";
														}
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 7m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													ulong num155 = num2;
													if (num155 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num155 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num155 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
													else if (num155 == (ulong)(b3 - 3))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														num2 = b3;
														b2 = 4;
													}
													else if (num155 == (ulong)(b3 - 4))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														num2 = b3;
														b2 = 5;
													}
													else if (num155 == (ulong)(b3 - 5))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														num2 = b3;
														b2 = 6;
													}
													else if (num155 == (ulong)(b3 - 6))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
														array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
														array[7] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))];
														num2 = b3;
														b2 = 7;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63576m) == 0)
											{
												int selectedIndex118 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex118 == 8 || selectedIndex118 == 11)
												{
													b6 = 4;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														text3 = ((array2[2] < 128) ? (text3 + "[補正有主人公能力変化,種類0x" + $"{array2[1]:X2}" + ",+" + Conversions.ToString(array2[2]) + "]") : (text3 + "[補正有主人公能力変化,種類0x" + $"{array2[1]:X2}" + ",-" + Conversions.ToString(array2[2]) + "]"));
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num156 = num2;
														if (num156 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num156 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num156 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
													}
													break;
												}
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[F858]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num157 = num2;
													if (num157 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63577m) == 0)
											{
												int selectedIndex119 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex119 == 8 || selectedIndex119 == 11)
												{
													b6 = 4;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														text3 = ((array2[2] < 128) ? (text3 + "[補正無主人公能力変化,種類0x" + $"{array2[1]:X2}" + ",+" + Conversions.ToString(array2[2]) + "]") : (text3 + "[補正無主人公能力変化,種類0x" + $"{array2[1]:X2}" + ",-" + Conversions.ToString(array2[2]) + "]"));
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num158 = num2;
														if (num158 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num158 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num158 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
													}
													break;
												}
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[F859]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num159 = num2;
													if (num159 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63578m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													text3 = text3 + "[文字色" + Conversions.ToString(array2[1]) + "]";
													b2 = 0;
													b5 = 1;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													break;
												}
												ulong num160 = num2;
												if (num160 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num160 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												break;
											}
											if (decimal.Compare(d3, 63579m) == 0)
											{
												b6 = 4;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													text3 = text3 + "[数値代入," + Conversions.ToString(array2[1]) + "番目=" + Conversions.ToString(array2[2]) + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num161 = num2;
													if (num161 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num161 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num161 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63580m) == 0)
											{
												b6 = 4;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													text3 = text3 + "[数値加算," + Conversions.ToString(array2[1]) + "番目+" + Conversions.ToString(array2[2]) + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num162 = num2;
													if (num162 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num162 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num162 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63581m) == 0)
											{
												b6 = 4;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													text3 = text3 + "[数値減算," + Conversions.ToString(array2[1]) + "番目-" + Conversions.ToString(array2[2]) + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num163 = num2;
													if (num163 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num163 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num163 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63582m) == 0)
											{
												b6 = 4;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													text3 = text3 + "[GBA乱数3," + Conversions.ToString(array2[1]) + "番目=0～" + Conversions.ToString(array2[2]) + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num164 = num2;
													if (num164 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num164 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num164 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63583m) == 0)
											{
												b6 = 4;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													text3 = text3 + "[F85F,0x" + $"{array2[1]:X2}" + ",0x" + $"{array2[2]:X2}" + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num165 = num2;
													if (num165 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num165 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num165 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63584m) == 0)
											{
												b6 = 4;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													text3 = text3 + "[F860,0x" + $"{array2[1]:X2}" + ",0x" + $"{array2[2]:X2}" + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num166 = num2;
													if (num166 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num166 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num166 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63585m) == 0)
											{
												b6 = 4;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													text3 = text3 + "[F861,0x" + $"{array2[1]:X2}" + ",0x" + $"{array2[2]:X2}" + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num167 = num2;
													if (num167 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num167 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num167 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63586m) == 0)
											{
												b6 = 7;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))])));
													if (array2[2] >= 2147483648u)
													{
														array2[2] -= 4294967296L;
													}
													text3 = text3 + "[数値代入," + Conversions.ToString(array2[1]) + "番目=" + Conversions.ToString(array2[2]) + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 6m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
													break;
												}
												ulong num168 = num2;
												if (num168 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num168 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num168 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
												else if (num168 == (ulong)(b3 - 3))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													num2 = b3;
													b2 = 4;
												}
												else if (num168 == (ulong)(b3 - 4))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
													num2 = b3;
													b2 = 5;
												}
												else if (num168 == (ulong)(b3 - 5))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
													array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
													num2 = b3;
													b2 = 6;
												}
												break;
											}
											if (decimal.Compare(d3, 63587m) == 0)
											{
												b6 = 7;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))])));
													text3 = text3 + "[数値加算," + Conversions.ToString(array2[1]) + "番目+" + Conversions.ToString(array2[2]) + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 6m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
													break;
												}
												ulong num169 = num2;
												if (num169 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num169 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num169 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
												else if (num169 == (ulong)(b3 - 3))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													num2 = b3;
													b2 = 4;
												}
												else if (num169 == (ulong)(b3 - 4))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
													num2 = b3;
													b2 = 5;
												}
												else if (num169 == (ulong)(b3 - 5))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
													array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
													num2 = b3;
													b2 = 6;
												}
												break;
											}
											if (decimal.Compare(d3, 63588m) == 0)
											{
												b6 = 7;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))])));
													text3 = text3 + "[数値減算," + Conversions.ToString(array2[1]) + "番目-" + Conversions.ToString(array2[2]) + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 6m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
													break;
												}
												ulong num170 = num2;
												if (num170 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num170 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num170 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
												else if (num170 == (ulong)(b3 - 3))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													num2 = b3;
													b2 = 4;
												}
												else if (num170 == (ulong)(b3 - 4))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
													num2 = b3;
													b2 = 5;
												}
												else if (num170 == (ulong)(b3 - 5))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
													array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
													num2 = b3;
													b2 = 6;
												}
												break;
											}
											if (decimal.Compare(d3, 63589m) == 0)
											{
												b6 = 7;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))])));
													text3 = text3 + "[DS64bit乱数," + Conversions.ToString(array2[1]) + "番目=0～" + Conversions.ToString(array2[2]) + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 6m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
													break;
												}
												ulong num171 = num2;
												if (num171 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num171 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num171 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
												else if (num171 == (ulong)(b3 - 3))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													num2 = b3;
													b2 = 4;
												}
												else if (num171 == (ulong)(b3 - 4))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
													num2 = b3;
													b2 = 5;
												}
												else if (num171 == (ulong)(b3 - 5))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
													array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
													num2 = b3;
													b2 = 6;
												}
												break;
											}
											if (decimal.Compare(d3, 63590m) == 0)
											{
												b6 = 7;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))])));
													text3 = text3 + "[F866," + Conversions.ToString(array2[1]) + "番目,0x" + $"{array2[2]:X8}" + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 6m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
													break;
												}
												ulong num172 = num2;
												if (num172 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num172 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num172 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
												else if (num172 == (ulong)(b3 - 3))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													num2 = b3;
													b2 = 4;
												}
												else if (num172 == (ulong)(b3 - 4))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
													num2 = b3;
													b2 = 5;
												}
												else if (num172 == (ulong)(b3 - 5))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
													array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
													num2 = b3;
													b2 = 6;
												}
												break;
											}
											if (decimal.Compare(d3, 63591m) == 0)
											{
												b6 = 4;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													text3 = text3 + "[アドレス数値代入2," + Conversions.ToString(array2[1]) + "番目=" + Conversions.ToString(array2[2]) + "番目]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num173 = num2;
													if (num173 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num173 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num173 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63592m) == 0)
											{
												b6 = 7;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array2[2] = Convert.ToInt64(decimal.Add(decimal.Add(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))]), 16777216m), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))]), 65536m)), decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))]), 256m)), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 6m))])));
													text3 = text3 + "[フラグ書込," + Conversions.ToString(array2[1]) + "番目,0x" + $"{array2[2]:X8}" + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 6m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
													break;
												}
												ulong num174 = num2;
												if (num174 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num174 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num174 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
												else if (num174 == (ulong)(b3 - 3))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													num2 = b3;
													b2 = 4;
												}
												else if (num174 == (ulong)(b3 - 4))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
													num2 = b3;
													b2 = 5;
												}
												else if (num174 == (ulong)(b3 - 5))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													array[4] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
													array[5] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 4m))];
													array[6] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 5m))];
													num2 = b3;
													b2 = 6;
												}
												break;
											}
											if (decimal.Compare(d3, 63593m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													text3 = text3 + "[1Byte数値表示," + Conversions.ToString(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]) + "番目]";
													b2 = 0;
													b5 = 1;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													break;
												}
												ulong num175 = num2;
												if (num175 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num175 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												break;
											}
											if (decimal.Compare(d3, 63594m) == 0)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													text3 = text3 + "[4Byte数値表示," + Conversions.ToString(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]) + "番目]";
													b2 = 0;
													b5 = 1;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													break;
												}
												ulong num176 = num2;
												if (num176 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num176 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												break;
											}
											if (decimal.Compare(d3, 63595m) == 0)
											{
												int selectedIndex120 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex120 >= 5 && selectedIndex120 <= 7)
												{
													b6 = 3;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														text3 = text3 + "[左絵服変更0x" + $"{array2[1]:X2}" + "]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num177 = num2;
														if (num177 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num177 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
													}
													break;
												}
												if (selectedIndex120 == 9 || (selectedIndex120 >= 11 && selectedIndex120 <= 17))
												{
													b6 = 3;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														text3 = text3 + "[吹出0x" + $"{array2[1]:X2}" + "]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num178 = num2;
														if (num178 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num178 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
													}
													break;
												}
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[F86B]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num179 = num2;
													if (num179 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63596m) == 0)
											{
												int selectedIndex121 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex121 >= 5 && selectedIndex121 <= 7)
												{
													b6 = 3;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														text3 = text3 + "[右絵服変更0x" + $"{array2[1]:X2}" + "]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num180 = num2;
														if (num180 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num180 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
													}
													break;
												}
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[F86C]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num181 = num2;
													if (num181 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63597m) == 0)
											{
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													text3 += "[ルビ]【";
													b2 = 0;
													b5 = 1;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													break;
												}
												ulong num182 = num2;
												if (num182 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												break;
											}
											if (decimal.Compare(d3, 63598m) == 0)
											{
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													text3 += "】";
													b2 = 0;
													b5 = 1;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													break;
												}
												ulong num183 = num2;
												if (num183 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												break;
											}
											if (decimal.Compare(d3, 63599m) == 0)
											{
												b6 = 4;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))])));
													text3 = text3 + "[F86F,0x" + $"{array2[1]:X4}" + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
													break;
												}
												ulong num184 = num2;
												if (num184 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num184 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												else if (num184 == (ulong)(b3 - 2))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
													num2 = b3;
													b2 = 3;
												}
												break;
											}
											if (decimal.Compare(d3, 63600m) == 0)
											{
												int selectedIndex122 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex122 == 8 || selectedIndex122 == 11)
												{
													b6 = 4;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														text3 = ((array2[2] < 128) ? (text3 + "[補正有部員能力変化,種類0x" + $"{array2[1]:X2}" + ",+" + Conversions.ToString(array2[2]) + "]") : (text3 + "[補正有部員能力変化,種類0x" + $"{array2[1]:X2}" + ",-" + Conversions.ToString(array2[2]) + "]"));
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num185 = num2;
														if (num185 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num185 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num185 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
													}
													break;
												}
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[F870]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num186 = num2;
													if (num186 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63601m) == 0)
											{
												int selectedIndex123 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex123 == 8 || selectedIndex123 == 11)
												{
													b6 = 4;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														array2[2] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
														text3 = ((array2[2] < 128) ? (text3 + "[補正無部員能力変化,種類0x" + $"{array2[1]:X2}" + ",+" + Conversions.ToString(array2[2]) + "]") : (text3 + "[補正無部員能力変化,種類0x" + $"{array2[1]:X2}" + ",-" + Conversions.ToString(array2[2]) + "]"));
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num187 = num2;
														if (num187 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num187 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
														else if (num187 == (ulong)(b3 - 2))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
															num2 = b3;
															b2 = 3;
														}
													}
													break;
												}
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[F871]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num188 = num2;
													if (num188 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63602m) == 0)
											{
												int selectedIndex124 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex124 == 8 || selectedIndex124 == 11)
												{
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														text3 += "[部員名]";
														b2 = 0;
														b5 = 1;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														break;
													}
													ulong num189 = num2;
													if (num189 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													break;
												}
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[F872]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num190 = num2;
													if (num190 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63603m) == 0)
											{
												int selectedIndex125 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex125 == 8 || selectedIndex125 == 11)
												{
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														text3 += "[高校名]";
														b2 = 0;
														b5 = 1;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														break;
													}
													ulong num191 = num2;
													if (num191 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													break;
												}
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[F873]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num192 = num2;
													if (num192 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63604m) == 0)
											{
												int selectedIndex126 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex126 == 8 || selectedIndex126 == 11)
												{
													b6 = 3;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														text3 = text3 + "[左絵0x" + $"{array2[1]:X2}" + "]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num193 = num2;
														if (num193 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num193 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
													}
													break;
												}
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[F874]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num194 = num2;
													if (num194 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63608m) == 0)
											{
												int selectedIndex127 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex127 == 8 || selectedIndex127 == 11)
												{
													b6 = 3;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														text3 = text3 + "[右絵0x" + $"{array2[1]:X2}" + "]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num195 = num2;
														if (num195 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num195 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
													}
													break;
												}
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[F878]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num196 = num2;
													if (num196 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63614m) == 0)
											{
												int selectedIndex128 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex128 == 8 || selectedIndex128 == 11)
												{
													b6 = 3;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														text3 = text3 + "[吹出0x" + $"{array2[1]:X2}" + "]";
														b2 = 0;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
														if (b == 0)
														{
															text3 += "\r\n";
														}
													}
													else
													{
														ulong num197 = num2;
														if (num197 == b3)
														{
															array[1] = array[(int)num2];
															num2 = b3;
															b2 = 1;
														}
														else if (num197 == (ulong)(b3 - 1))
														{
															array[1] = array[(int)num2];
															array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
															num2 = b3;
															b2 = 2;
														}
													}
													break;
												}
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[F87E]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num198 = num2;
													if (num198 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63616m) == 0)
											{
												int selectedIndex129 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex129 == 8 || selectedIndex129 == 11)
												{
													b6 = 2;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														text3 += "[県名]";
														b2 = 0;
														b5 = 1;
														num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														break;
													}
													ulong num199 = num2;
													if (num199 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													break;
												}
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[F880]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num200 = num2;
													if (num200 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63617m) == 0)
											{
												int selectedIndex130 = 文字コード選択ComboBox.SelectedIndex;
												if (selectedIndex130 == 8 || selectedIndex130 == 11)
												{
													b6 = 4;
													if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
													{
														if (unchecked(b5 == 1 && b == 0))
														{
															text3 += "\r\n";
															b5 = 0;
														}
														if (decimal.Compare(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))]), 129m) == 0)
														{
															array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 3m))];
															text3 = text3 + "[F88181,0x" + $"{array2[1]:X2}" + "]";
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 3m));
														}
														else
														{
															text3 += "[F881]";
															num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
														}
														b2 = 0;
														if (b == 0)
														{
															text3 += "\r\n";
														}
														break;
													}
													ulong num201 = num2;
													if (num201 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num201 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
													else if (num201 == (ulong)(b3 - 2))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														array[3] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))];
														num2 = b3;
														b2 = 3;
													}
													break;
												}
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[F881]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num202 = num2;
													if (num202 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											if (decimal.Compare(d3, 63736m) == 0)
											{
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													text3 += "[択端]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num203 = num2;
													if (num203 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
												break;
											}
											b6 = 2;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[(int)num2]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))])));
												text3 = text3 + "[" + $"{array2[1]:X4}" + "]";
												b2 = 0;
												num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
												if (b == 0)
												{
													text3 += "\r\n";
												}
											}
											else
											{
												ulong num204 = num2;
												if (num204 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
											}
											break;
										}
										case 249uL:
											text3 += " ";
											b2 = 0;
											b5 = 1;
											break;
										case 250uL:
											text3 += "[改行]";
											b2 = 0;
											b5 = 0;
											if (b == 0)
											{
												text3 += "\r\n";
											}
											break;
										case 251uL:
											text3 += "▼[改行]";
											b2 = 0;
											b5 = 0;
											if (b == 0)
											{
												text3 += "\r\n";
											}
											break;
										case 252uL:
										{
											int selectedIndex61 = 文字コード選択ComboBox.SelectedIndex;
											if (selectedIndex61 == 2 || selectedIndex61 == 3)
											{
												byte b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													text3 = text3 + "[中絵0x" + $"{array2[1]:X2}" + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num30 = num2;
													if (num30 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
											}
											else if ((selectedIndex61 >= 4 && selectedIndex61 <= 7) || selectedIndex61 == 8 || selectedIndex61 == 11)
											{
												byte b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													text3 = text3 + "[大背景0x" + $"{array2[1]:X2}" + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num31 = num2;
													if (num31 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
												}
											}
											else if (selectedIndex61 == 9 || (selectedIndex61 >= 12 && selectedIndex61 <= 17))
											{
												byte b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
													text3 = text3 + "[大背景0x" + $"{array2[1]:X4}" + "]";
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num32 = num2;
													if (num32 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num32 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
												}
											}
											else
											{
												if (selectedIndex61 != 10)
												{
													break;
												}
												byte b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
													long num33 = array2[1];
													text3 = ((num33 >= 0 && num33 <= 21) ? (text3 + "[大背景0x" + $"{array2[1]:X4}" + "]") : (num33 switch
													{
														22L => text3 + "[大背景黒フェード]", 
														23L => text3 + "[大背景白フェード]", 
														184L => text3 + "[小背景フェードイン]", 
														185L => text3 + "[小背景フェードアウト]", 
														_ => text3 + "[小背景0x" + $"{array2[1]:X4}" + "]", 
													}));
													b2 = 0;
													num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
													if (b == 0)
													{
														text3 += "\r\n";
													}
												}
												else
												{
													ulong num34 = num2;
													if (num34 == b3)
													{
														array[1] = array[(int)num2];
														num2 = b3;
														b2 = 1;
													}
													else if (num34 == (ulong)(b3 - 1))
													{
														array[1] = array[(int)num2];
														array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
														num2 = b3;
														b2 = 2;
													}
												}
											}
											break;
										}
										case 253uL:
										{
											int selectedIndex60 = 文字コード選択ComboBox.SelectedIndex;
											byte b6;
											if ((selectedIndex60 >= 2 && selectedIndex60 <= 7) || selectedIndex60 == 8 || selectedIndex60 == 11)
											{
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													long num21 = array2[1];
													unchecked
													{
														long num22 = num21 - 247;
														if ((ulong)num22 > 8uL)
														{
															goto IL_2445c;
														}
														switch (num22)
														{
														case 0L:
															break;
														case 1L:
															goto IL_243ce;
														case 2L:
															goto IL_243e2;
														case 3L:
															goto IL_243f6;
														case 4L:
															goto IL_24407;
														case 5L:
															goto IL_24418;
														case 6L:
															goto IL_24429;
														case 7L:
															goto IL_2443a;
														case 8L:
															goto IL_2444b;
														default:
															goto IL_2445c;
														}
														text3 += "[左絵フェードイン最遅]";
														goto IL_24485;
													}
												}
												ulong num23 = num2;
												if (num23 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												break;
											}
											if (selectedIndex60 == 10)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													unchecked
													{
														if (b5 == 1 && b == 0)
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
														long num24 = array2[1];
														long num25 = num24 - 254;
														if ((ulong)num25 > 14uL)
														{
															goto IL_2474a;
														}
														switch (num25)
														{
														case 0L:
															break;
														case 1L:
															goto IL_24658;
														case 2L:
															goto IL_2466c;
														case 4L:
															goto IL_24680;
														case 5L:
															goto IL_24694;
														case 6L:
															goto IL_246a8;
														case 7L:
															goto IL_246bc;
														case 8L:
															goto IL_246d0;
														case 9L:
															goto IL_246e4;
														case 10L:
															goto IL_246f5;
														case 11L:
															goto IL_24706;
														case 12L:
															goto IL_24717;
														case 13L:
															goto IL_24728;
														case 14L:
															goto IL_24739;
														default:
															goto IL_2474a;
														}
														text3 += "[左絵なし]";
														goto IL_24773;
													}
												}
												ulong num26 = num2;
												if (num26 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num26 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												break;
											}
											if (selectedIndex60 != 9 && (selectedIndex60 < 12 || selectedIndex60 > 17))
											{
												break;
											}
											b6 = 3;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												unchecked
												{
													if (b5 == 1 && b == 0)
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
													long num27 = array2[1];
													if (num27 != 0L)
													{
														long num28 = num27 - 65530;
														if ((ulong)num28 > 5uL)
														{
															goto IL_249fc;
														}
														switch (num28)
														{
														case 0L:
															break;
														case 1L:
															goto IL_249a7;
														case 2L:
															goto IL_249b8;
														case 3L:
															goto IL_249c9;
														case 4L:
															goto IL_249da;
														case 5L:
															goto IL_249eb;
														default:
															goto IL_249fc;
														}
														text3 += "[左絵ブルブル]";
													}
													else
													{
														text3 += "[左絵なし]";
													}
													goto IL_24a25;
												}
											}
											ulong num29 = num2;
											if (num29 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num29 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											break;
										}
										case 254uL:
										{
											int selectedIndex59 = 文字コード選択ComboBox.SelectedIndex;
											byte b6;
											if ((selectedIndex59 >= 2 && selectedIndex59 <= 7) || selectedIndex59 == 8 || selectedIndex59 == 11)
											{
												b6 = 2;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													if (unchecked(b5 == 1 && b == 0))
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = (long)array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													long num12 = array2[1];
													unchecked
													{
														long num13 = num12 - 247;
														if ((ulong)num13 > 8uL)
														{
															goto IL_24cc4;
														}
														switch (num13)
														{
														case 0L:
															break;
														case 1L:
															goto IL_24c36;
														case 2L:
															goto IL_24c4a;
														case 3L:
															goto IL_24c5e;
														case 4L:
															goto IL_24c6f;
														case 5L:
															goto IL_24c80;
														case 6L:
															goto IL_24c91;
														case 7L:
															goto IL_24ca2;
														case 8L:
															goto IL_24cb3;
														default:
															goto IL_24cc4;
														}
														text3 += "[右絵フェードイン最遅]";
														goto IL_24ced;
													}
												}
												ulong num14 = num2;
												if (num14 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												break;
											}
											if (selectedIndex59 == 10)
											{
												b6 = 3;
												if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
												{
													unchecked
													{
														if (b5 == 1 && b == 0)
														{
															text3 += "\r\n";
															b5 = 0;
														}
														array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
														long num15 = array2[1];
														long num16 = num15 - 254;
														if ((ulong)num16 > 14uL)
														{
															goto IL_24fb2;
														}
														switch (num16)
														{
														case 0L:
															break;
														case 1L:
															goto IL_24ec0;
														case 2L:
															goto IL_24ed4;
														case 4L:
															goto IL_24ee8;
														case 5L:
															goto IL_24efc;
														case 6L:
															goto IL_24f10;
														case 7L:
															goto IL_24f24;
														case 8L:
															goto IL_24f38;
														case 9L:
															goto IL_24f4c;
														case 10L:
															goto IL_24f5d;
														case 11L:
															goto IL_24f6e;
														case 12L:
															goto IL_24f7f;
														case 13L:
															goto IL_24f90;
														case 14L:
															goto IL_24fa1;
														default:
															goto IL_24fb2;
														}
														text3 += "[右絵なし]";
														goto IL_24fdb;
													}
												}
												ulong num17 = num2;
												if (num17 == b3)
												{
													array[1] = array[(int)num2];
													num2 = b3;
													b2 = 1;
												}
												else if (num17 == (ulong)(b3 - 1))
												{
													array[1] = array[(int)num2];
													array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
													num2 = b3;
													b2 = 2;
												}
												break;
											}
											if (selectedIndex59 != 9 && (selectedIndex59 < 12 || selectedIndex59 > 17))
											{
												break;
											}
											b6 = 3;
											if (decimal.Compare(new decimal(num2), new decimal((byte)unchecked((uint)(b3 - b6)) + 1)) <= 0)
											{
												unchecked
												{
													if (b5 == 1 && b == 0)
													{
														text3 += "\r\n";
														b5 = 0;
													}
													array2[1] = Convert.ToInt64(decimal.Add(decimal.Multiply(new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))]), 256m), new decimal(array[Convert.ToInt32(decimal.Add(new decimal(num2), 2m))])));
													long num18 = array2[1];
													if (num18 != 0L)
													{
														long num19 = num18 - 65530;
														if ((ulong)num19 > 5uL)
														{
															goto IL_25264;
														}
														switch (num19)
														{
														case 0L:
															break;
														case 1L:
															goto IL_2520f;
														case 2L:
															goto IL_25220;
														case 3L:
															goto IL_25231;
														case 4L:
															goto IL_25242;
														case 5L:
															goto IL_25253;
														default:
															goto IL_25264;
														}
														text3 += "[右絵ブルブル]";
													}
													else
													{
														text3 += "[右絵なし]";
													}
													goto IL_2528d;
												}
											}
											ulong num20 = num2;
											if (num20 == b3)
											{
												array[1] = array[(int)num2];
												num2 = b3;
												b2 = 1;
											}
											else if (num20 == (ulong)(b3 - 1))
											{
												array[1] = array[(int)num2];
												array[2] = array[Convert.ToInt32(decimal.Add(new decimal(num2), 1m))];
												num2 = b3;
												b2 = 2;
											}
											break;
										}
										case 255uL:
											{
												if (unchecked(b5 == 1 && b == 0))
												{
													text3 += "\r\n";
													b5 = 0;
												}
												text3 += "[終端]";
												b2 = 0;
												if (b == 0)
												{
													text3 += "\r\n";
												}
												break;
											}
											IL_24ced:
											b2 = 0;
											num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
											if (b == 0)
											{
												text3 += "\r\n";
											}
											break;
											IL_2443a:
											text3 += "[左絵フェードアウト最速]";
											goto IL_24485;
											IL_2444b:
											text3 += "[左絵なし]";
											goto IL_24485;
											IL_249fc:
											text3 = text3 + "[左絵0x" + $"{array2[1]:X4}" + "]";
											goto IL_24a25;
											IL_24407:
											text3 += "[左絵フェードアウト最遅]";
											goto IL_24485;
											IL_249eb:
											text3 += "[左絵前走去]";
											goto IL_24a25;
											IL_249c9:
											text3 += "[左絵逆向]";
											goto IL_24a25;
											IL_24418:
											text3 += "[左絵フェードアウト遅]";
											goto IL_24485;
											IL_24a25:
											b2 = 0;
											num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
											if (b == 0)
											{
												text3 += "\r\n";
											}
											break;
											IL_243e2:
											text3 += "[左絵フェードイン速]";
											goto IL_24485;
											IL_24fb2:
											text3 = text3 + "[右絵0x" + $"{array2[1]:X4}" + "]";
											goto IL_24fdb;
											IL_24fa1:
											text3 += "[右絵ブルブル]";
											goto IL_24fdb;
											IL_24f90:
											text3 += "[右絵後へ走去]";
											goto IL_24fdb;
											IL_24f7f:
											text3 += "[右絵フラッシュ]";
											goto IL_24fdb;
											IL_24f6e:
											text3 += "[右絵フェードアウト最速]";
											goto IL_24fdb;
											IL_24f5d:
											text3 += "[右絵フェードアウト速]";
											goto IL_24fdb;
											IL_24f4c:
											text3 += "[右絵フェードアウト遅]";
											goto IL_24fdb;
											IL_24f38:
											text3 += "[右絵フェードアウト最遅]";
											goto IL_24fdb;
											IL_24f24:
											text3 += "[右絵フェードイン最速]";
											goto IL_24fdb;
											IL_24f10:
											text3 += "[右絵フェードイン速]";
											goto IL_24fdb;
											IL_24efc:
											text3 += "[右絵フェードイン遅]";
											goto IL_24fdb;
											IL_24ee8:
											text3 += "[右絵フェードイン最遅]";
											goto IL_24fdb;
											IL_24ed4:
											text3 += "[右絵右へ戻る]";
											goto IL_24fdb;
											IL_24ec0:
											text3 += "[右絵中央移動]";
											goto IL_24fdb;
											IL_2474a:
											text3 = text3 + "[左絵0x" + $"{array2[1]:X4}" + "]";
											goto IL_24773;
											IL_24fdb:
											b2 = 0;
											num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
											if (b == 0)
											{
												text3 += "\r\n";
											}
											break;
											IL_24739:
											text3 += "[左絵ブルブル]";
											goto IL_24773;
											IL_249a7:
											text3 += "[左絵フェードアウト]";
											goto IL_24a25;
											IL_24728:
											text3 += "[左絵後へ走去]";
											goto IL_24773;
											IL_24717:
											text3 += "[左絵フラッシュ]";
											goto IL_24773;
											IL_24706:
											text3 += "[左絵フェードアウト最速]";
											goto IL_24773;
											IL_249da:
											text3 += "[左絵後走去]";
											goto IL_24a25;
											IL_246e4:
											text3 += "[左絵フェードアウト遅]";
											goto IL_24773;
											IL_246d0:
											text3 += "[左絵フェードアウト最遅]";
											goto IL_24773;
											IL_246f5:
											text3 += "[左絵フェードアウト速]";
											goto IL_24773;
											IL_246bc:
											text3 += "[左絵フェードイン最速]";
											goto IL_24773;
											IL_24680:
											text3 += "[左絵フェードイン最遅]";
											goto IL_24773;
											IL_24694:
											text3 += "[左絵フェードイン遅]";
											goto IL_24773;
											IL_2466c:
											text3 += "[左絵左へ戻る]";
											goto IL_24773;
											IL_2445c:
											text3 = text3 + "[左絵0x" + $"{array2[1]:X2}" + "]";
											goto IL_24485;
											IL_25264:
											text3 = text3 + "[右絵0x" + $"{array2[1]:X4}" + "]";
											goto IL_2528d;
											IL_25253:
											text3 += "[右絵前走去]";
											goto IL_2528d;
											IL_25242:
											text3 += "[右絵後走去]";
											goto IL_2528d;
											IL_25231:
											text3 += "[右絵逆向]";
											goto IL_2528d;
											IL_25220:
											text3 += "[右絵フェードイン]";
											goto IL_2528d;
											IL_2520f:
											text3 += "[右絵フェードアウト]";
											goto IL_2528d;
											IL_24773:
											b2 = 0;
											num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
											if (b == 0)
											{
												text3 += "\r\n";
											}
											break;
											IL_24658:
											text3 += "[左絵中央移動]";
											goto IL_24773;
											IL_2528d:
											b2 = 0;
											num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 2m));
											if (b == 0)
											{
												text3 += "\r\n";
											}
											break;
											IL_243ce:
											text3 += "[左絵フェードイン遅]";
											goto IL_24485;
											IL_246a8:
											text3 += "[左絵フェードイン速]";
											goto IL_24773;
											IL_243f6:
											text3 += "[左絵フェードイン最速]";
											goto IL_24485;
											IL_24485:
											b2 = 0;
											num2 = Convert.ToUInt64(decimal.Add(new decimal(num2), 1m));
											if (b == 0)
											{
												text3 += "\r\n";
											}
											break;
											IL_249b8:
											text3 += "[左絵フェードイン]";
											goto IL_24a25;
											IL_24429:
											text3 += "[左絵フェードアウト速]";
											goto IL_24485;
											IL_24cc4:
											text3 = text3 + "[右絵0x" + $"{array2[1]:X2}" + "]";
											goto IL_24ced;
											IL_24cb3:
											text3 += "[右絵なし]";
											goto IL_24ced;
											IL_24ca2:
											text3 += "[右絵フェードアウト最速]";
											goto IL_24ced;
											IL_24c91:
											text3 += "[右絵フェードアウト速]";
											goto IL_24ced;
											IL_24c80:
											text3 += "[右絵フェードアウト遅]";
											goto IL_24ced;
											IL_24c6f:
											text3 += "[右絵フェードアウト最遅]";
											goto IL_24ced;
											IL_24c5e:
											text3 += "[右絵フェードイン最速]";
											goto IL_24ced;
											IL_24c4a:
											text3 += "[右絵フェードイン速]";
											goto IL_24ced;
											IL_24c36:
											text3 += "[右絵フェードイン遅]";
											goto IL_24ced;
										}
									}
									Application.DoEvents();
								}
								if (アドレス化表示CheckBox.Checked)
								{
									array5[1] = Conversion.Hex(array3[4]) + Conversion.Hex(array3[3]) + Conversion.Hex(array3[2]) + Conversion.Hex(array3[1]);
									array5[2] = Conversion.Hex(array3[8]) + Conversion.Hex(array3[7]) + Conversion.Hex(array3[6]) + Conversion.Hex(array3[5]);
									array5[3] = Conversion.Hex(array3[12]) + Conversion.Hex(array3[11]) + Conversion.Hex(array3[10]) + Conversion.Hex(array3[9]);
									array5[4] = Conversion.Hex(array3[16]) + Conversion.Hex(array3[15]) + Conversion.Hex(array3[14]) + Conversion.Hex(array3[13]);
									text3 = text3 + " 0x" + array5[1] + " 0x 0x" + array5[2] + " 0x" + array5[3] + " 0x" + array5[4];
								}
								if (b != 0)
								{
									text3 += "\r\n";
								}
								if ((decimal.Compare(new decimal(num8), 1m) >= 0) & (Operators.CompareString(Strings.Mid(text3, Convert.ToInt32(decimal.Add(new decimal(value), 1m)), 16), "\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000", TextCompare: false) != 0))
								{
									text += text3;
									Application.DoEvents();
								}
							}
							Text = "処理データ:" + Conversions.ToString(num7) + "/" + Conversions.ToString(num6) + " 蓄積データ:" + Conversions.ToString(num3) + "/" + Conversions.ToString(蓄積データ出力NumericUpDown.Value) + " 処理中アドレス:" + Strings.Mid(str, 1, 8);
							Update();
							処理進行状況.Value = (int)Conversion.Int((double)num7 / (double)num6 * 100.0);
							経過表示Label.Text = Conversions.ToString(Conversion.Int((double)num7 / (double)num6 * 100.0)) + "%";
							if (decimal.Compare(new decimal(num3), 蓄積データ出力NumericUpDown.Value) >= 0)
							{
								if (Operators.CompareString(text, "", TextCompare: false) != 0)
								{
									MyProject.Computer.FileSystem.WriteAllText(Strings.Replace(参照ファイル名表示.Text, ".DMP", "") + "(" + Conversions.ToString(num4) + ").txt", text, append: false);
									num4 = Convert.ToUInt64(decimal.Add(new decimal(num4), 1m));
									text = "";
								}
								num3 = 0uL;
								Application.DoEvents();
							}
							num = Convert.ToUInt64(Wait時間NumericUpDown.Value);
							if (decimal.Compare(new decimal(value2), 3m) >= 0)
							{
								num7 = Convert.ToUInt64(decimal.Add(new decimal(num7), 1m));
							}
							if (decimal.Compare(decimal.Remainder(new decimal(value2), Wait間隔NumericUpDown.Value), 0m) == 0)
							{
								Thread.Sleep((int)num);
							}
							if ((decimal.Compare(new decimal(num8), 1m) >= 0) & (Operators.CompareString(Strings.Mid(text3, Convert.ToInt32(decimal.Add(new decimal(value), 1m)), 16), "\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000", TextCompare: false) != 0))
							{
								num3 = Convert.ToUInt64(decimal.Add(new decimal(num3), 1m));
							}
							else
							{
								value3 = Convert.ToUInt64(decimal.Add(new decimal(value3), 1m));
							}
							if (decimal.Compare(new decimal(value3), Wait間隔NumericUpDown.Value) == 0)
							{
								value3 = 0uL;
								Thread.Sleep((int)num);
							}
							if (Operators.CompareString(実行.Text, "実行", TextCompare: false) == 0)
							{
								goto end_IL_258ea;
							}
							Application.DoEvents();
						}
						value2 = Convert.ToUInt64(decimal.Add(new decimal(value2), 1m));
						Application.DoEvents();
						continue;
						end_IL_258ea:
						break;
					}
					Application.DoEvents();
					if (Operators.CompareString(text, "", TextCompare: false) != 0)
					{
						MyProject.Computer.FileSystem.WriteAllText(Strings.Replace(参照ファイル名表示.Text, ".DMP", "") + "(" + Conversions.ToString(num4) + ").txt", text, append: false);
					}
				}
				Application.DoEvents();
				出力オプションGroupBox.Enabled = true;
				文字コード選択ComboBox.Enabled = true;
				参照ファイル名表示.Enabled = true;
				参照.Enabled = true;
				Text = "変換終了";
			}
		}

		private void ファイル選択_FileOk(object sender, CancelEventArgs e)
		{
			参照ファイル名表示.Text = ファイル選択.FileName;
		}

		private void PokeTEXT_Form_FormClosing(object sender, FormClosingEventArgs e)
		{
			if (Operators.CompareString(実行.Text, "中止", TextCompare: false) == 0)
			{
				MessageBox.Show(this, "プログラムを終了する時は処理を中止してから終了してください。", "終了エラー", MessageBoxButtons.OK, MessageBoxIcon.Hand);
				e.Cancel = true;
			}
			else
			{
				e.Cancel = false;
			}
		}

		private void PokeTEXT_Form_Load(object sender, EventArgs e)
		{
			Text = "PokeTEXT - Ver." + MyProject.Application.Info.Version.ToString();
		}

		[DebuggerNonUserCode]
		protected override void Dispose(bool disposing)
		{
			try
			{
				if (disposing && components != null)
				{
					components.Dispose();
				}
			}
			finally
			{
				base.Dispose(disposing);
			}
		}

		[System.Diagnostics.DebuggerStepThrough]
		private void InitializeComponent()
		{
			this.components = new System.ComponentModel.Container();
			this.参照 = new System.Windows.Forms.Button();
			this.処理進行状況 = new System.Windows.Forms.ProgressBar();
			this.参照ファイル名表示 = new System.Windows.Forms.TextBox();
			this.ファイル選択 = new System.Windows.Forms.OpenFileDialog();
			this.参照ファイルLabel = new System.Windows.Forms.Label();
			this.経過表示Label = new System.Windows.Forms.Label();
			this.実行 = new System.Windows.Forms.CheckBox();
			this.文字コード選択ComboBox = new System.Windows.Forms.ComboBox();
			this.文字コード選択Label = new System.Windows.Forms.Label();
			this.アドレスありCheckBox = new System.Windows.Forms.CheckBox();
			this.十六進データありCheckBox = new System.Windows.Forms.CheckBox();
			this.出力オプションGroupBox = new System.Windows.Forms.GroupBox();
			this.アドレス化表示CheckBox = new System.Windows.Forms.CheckBox();
			this.蓄積データ出力NumericUpDown = new System.Windows.Forms.NumericUpDown();
			this.蓄積データ出力Label = new System.Windows.Forms.Label();
			this.補足 = new System.Windows.Forms.ToolTip(this.components);
			this.Wait間隔NumericUpDown = new System.Windows.Forms.NumericUpDown();
			this.Wait時間NumericUpDown = new System.Windows.Forms.NumericUpDown();
			this.Wait間隔Label = new System.Windows.Forms.Label();
			this.Wait時間Label = new System.Windows.Forms.Label();
			this.出力オプションGroupBox.SuspendLayout();
			((System.ComponentModel.ISupportInitialize)this.蓄積データ出力NumericUpDown).BeginInit();
			((System.ComponentModel.ISupportInitialize)this.Wait間隔NumericUpDown).BeginInit();
			((System.ComponentModel.ISupportInitialize)this.Wait時間NumericUpDown).BeginInit();
			base.SuspendLayout();
			this.参照.Location = new System.Drawing.Point(512, 113);
			this.参照.Name = "参照";
			this.参照.Size = new System.Drawing.Size(110, 28);
			this.参照.TabIndex = 9;
			this.参照.Text = "参照";
			this.補足.SetToolTip(this.参照, "変換するDMPファイルを選択します。");
			this.参照.UseVisualStyleBackColor = true;
			this.処理進行状況.Location = new System.Drawing.Point(98, 147);
			this.処理進行状況.Name = "処理進行状況";
			this.処理進行状況.Size = new System.Drawing.Size(408, 28);
			this.処理進行状況.TabIndex = 11;
			this.参照ファイル名表示.Location = new System.Drawing.Point(98, 118);
			this.参照ファイル名表示.Name = "参照ファイル名表示";
			this.参照ファイル名表示.ReadOnly = true;
			this.参照ファイル名表示.Size = new System.Drawing.Size(408, 19);
			this.参照ファイル名表示.TabIndex = 8;
			this.ファイル選択.DefaultExt = "dmp";
			this.ファイル選択.Filter = "ダンプファイル|*.DMP";
			this.参照ファイルLabel.AutoSize = true;
			this.参照ファイルLabel.Location = new System.Drawing.Point(29, 121);
			this.参照ファイルLabel.Name = "参照ファイルLabel";
			this.参照ファイルLabel.Size = new System.Drawing.Size(63, 12);
			this.参照ファイルLabel.TabIndex = 7;
			this.参照ファイルLabel.Text = "参照ファイル";
			this.経過表示Label.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right;
			this.経過表示Label.Location = new System.Drawing.Point(63, 155);
			this.経過表示Label.Name = "経過表示Label";
			this.経過表示Label.Size = new System.Drawing.Size(29, 12);
			this.経過表示Label.TabIndex = 10;
			this.経過表示Label.Text = "0%";
			this.経過表示Label.TextAlign = System.Drawing.ContentAlignment.TopRight;
			this.実行.Appearance = System.Windows.Forms.Appearance.Button;
			this.実行.Location = new System.Drawing.Point(512, 147);
			this.実行.Name = "実行";
			this.実行.Size = new System.Drawing.Size(110, 28);
			this.実行.TabIndex = 12;
			this.実行.Text = "実行";
			this.実行.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
			this.補足.SetToolTip(this.実行, "文字コード選択で変換したい作品を選び、変換するDMPファイルを参照した後、「実行」のボタンを押してください。");
			this.実行.UseVisualStyleBackColor = true;
			this.文字コード選択ComboBox.FormattingEnabled = true;
			this.文字コード選択ComboBox.Items.AddRange(new object[18]
			{
				"パワプロクンポケット", "パワプロクンポケット2", "パワプロクンポケット3", "パワプロクンポケット4", "パワプロクンポケット5", "パワプロクンポケット6", "パワプロクンポケット1･2", "パワプロクンポケット7", "パワポケ甲子園", "パワプロクンポケット8",
				"パワポケダッシュ", "あつまれ!パワプロクンのDS甲子園", "パワプロクンポケット9", "パワプロクンポケット10", "パワプロクンポケット11", "パワプロクンポケット12", "パワプロクンポケット13", "パワプロクンポケット14"
			});
			this.文字コード選択ComboBox.Location = new System.Drawing.Point(98, 92);
			this.文字コード選択ComboBox.Name = "文字コード選択ComboBox";
			this.文字コード選択ComboBox.Size = new System.Drawing.Size(408, 20);
			this.文字コード選択ComboBox.TabIndex = 6;
			this.文字コード選択ComboBox.Text = "パワプロクンポケット14";
			this.補足.SetToolTip(this.文字コード選択ComboBox, "作品に合った文字コードを選択してください。");
			this.文字コード選択Label.AutoSize = true;
			this.文字コード選択Label.Location = new System.Drawing.Point(12, 95);
			this.文字コード選択Label.Name = "文字コード選択Label";
			this.文字コード選択Label.Size = new System.Drawing.Size(80, 12);
			this.文字コード選択Label.TabIndex = 5;
			this.文字コード選択Label.Text = "文字コード選択";
			this.アドレスありCheckBox.AutoSize = true;
			this.アドレスありCheckBox.Checked = true;
			this.アドレスありCheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
			this.アドレスありCheckBox.Location = new System.Drawing.Point(6, 18);
			this.アドレスありCheckBox.Name = "アドレスありCheckBox";
			this.アドレスありCheckBox.Size = new System.Drawing.Size(78, 16);
			this.アドレスありCheckBox.TabIndex = 0;
			this.アドレスありCheckBox.Text = "アドレスあり";
			this.補足.SetToolTip(this.アドレスありCheckBox, "出力するファイルに変換したアドレスを載せるか設定します。");
			this.アドレスありCheckBox.UseVisualStyleBackColor = true;
			this.十六進データありCheckBox.AutoSize = true;
			this.十六進データありCheckBox.Checked = true;
			this.十六進データありCheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
			this.十六進データありCheckBox.Location = new System.Drawing.Point(90, 18);
			this.十六進データありCheckBox.Name = "十六進データありCheckBox";
			this.十六進データありCheckBox.Size = new System.Drawing.Size(94, 16);
			this.十六進データありCheckBox.TabIndex = 1;
			this.十六進データありCheckBox.Text = "16進データあり";
			this.補足.SetToolTip(this.十六進データありCheckBox, "出力するファイルに変換するの前の16進数のデータを載せるか設定します。");
			this.十六進データありCheckBox.UseVisualStyleBackColor = true;
			this.出力オプションGroupBox.AutoSize = true;
			this.出力オプションGroupBox.Controls.Add(this.アドレス化表示CheckBox);
			this.出力オプションGroupBox.Controls.Add(this.蓄積データ出力NumericUpDown);
			this.出力オプションGroupBox.Controls.Add(this.蓄積データ出力Label);
			this.出力オプションGroupBox.Controls.Add(this.アドレスありCheckBox);
			this.出力オプションGroupBox.Controls.Add(this.十六進データありCheckBox);
			this.出力オプションGroupBox.Location = new System.Drawing.Point(12, 12);
			this.出力オプションGroupBox.Name = "出力オプションGroupBox";
			this.出力オプションGroupBox.Size = new System.Drawing.Size(358, 74);
			this.出力オプションGroupBox.TabIndex = 0;
			this.出力オプションGroupBox.TabStop = false;
			this.出力オプションGroupBox.Text = "出力オプション";
			this.補足.SetToolTip(this.出力オプションGroupBox, "処理の実行前に必要なオプションにチェックをしてください。\r\n全てチェック無しの場合は制御文字の適切な所に改行を入れて見やすく出力します。");
			this.アドレス化表示CheckBox.AutoSize = true;
			this.アドレス化表示CheckBox.Location = new System.Drawing.Point(6, 40);
			this.アドレス化表示CheckBox.Name = "アドレス化表示CheckBox";
			this.アドレス化表示CheckBox.Size = new System.Drawing.Size(96, 16);
			this.アドレス化表示CheckBox.TabIndex = 4;
			this.アドレス化表示CheckBox.Text = "アドレス化表示";
			this.補足.SetToolTip(this.アドレス化表示CheckBox, "出力するファイルに参照先であるアドレス化したデータを載せるか設定します。\r\nポケ3以降で有効。");
			this.アドレス化表示CheckBox.UseVisualStyleBackColor = true;
			this.蓄積データ出力NumericUpDown.Location = new System.Drawing.Point(277, 17);
			this.蓄積データ出力NumericUpDown.Maximum = new decimal(new int[4] { 1000000, 0, 0, 0 });
			this.蓄積データ出力NumericUpDown.Minimum = new decimal(new int[4] { 1000, 0, 0, 0 });
			this.蓄積データ出力NumericUpDown.Name = "蓄積データ出力NumericUpDown";
			this.蓄積データ出力NumericUpDown.Size = new System.Drawing.Size(75, 19);
			this.蓄積データ出力NumericUpDown.TabIndex = 3;
			this.蓄積データ出力NumericUpDown.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
			this.補足.SetToolTip(this.蓄積データ出力NumericUpDown, "PCへの負荷を考慮して一定量のデータが蓄積したらファイルを出力します。\r\n設定した量のデータが蓄積したらファイルを出力します。");
			this.蓄積データ出力NumericUpDown.Value = new decimal(new int[4] { 50000, 0, 0, 0 });
			this.蓄積データ出力Label.AutoSize = true;
			this.蓄積データ出力Label.Location = new System.Drawing.Point(190, 19);
			this.蓄積データ出力Label.Name = "蓄積データ出力Label";
			this.蓄積データ出力Label.Size = new System.Drawing.Size(81, 12);
			this.蓄積データ出力Label.TabIndex = 2;
			this.蓄積データ出力Label.Text = "蓄積データ出力";
			this.Wait間隔NumericUpDown.Location = new System.Drawing.Point(433, 29);
			this.Wait間隔NumericUpDown.Maximum = new decimal(new int[4] { 1000000, 0, 0, 0 });
			this.Wait間隔NumericUpDown.Minimum = new decimal(new int[4] { 1000, 0, 0, 0 });
			this.Wait間隔NumericUpDown.Name = "Wait間隔NumericUpDown";
			this.Wait間隔NumericUpDown.Size = new System.Drawing.Size(75, 19);
			this.Wait間隔NumericUpDown.TabIndex = 2;
			this.Wait間隔NumericUpDown.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
			this.補足.SetToolTip(this.Wait間隔NumericUpDown, "PCへの負荷を考慮してWait間隔を設定します。\r\n設定した数値のデータを処理する毎にWaitをかけます。\r\n最速値は1000000です。");
			this.Wait間隔NumericUpDown.Value = new decimal(new int[4] { 5000, 0, 0, 0 });
			this.Wait時間NumericUpDown.Location = new System.Drawing.Point(571, 29);
			this.Wait時間NumericUpDown.Maximum = new decimal(new int[4] { 1000, 0, 0, 0 });
			this.Wait時間NumericUpDown.Minimum = new decimal(new int[4] { 1, 0, 0, 0 });
			this.Wait時間NumericUpDown.Name = "Wait時間NumericUpDown";
			this.Wait時間NumericUpDown.Size = new System.Drawing.Size(51, 19);
			this.Wait時間NumericUpDown.TabIndex = 4;
			this.Wait時間NumericUpDown.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
			this.補足.SetToolTip(this.Wait時間NumericUpDown, "PCへの負荷を考慮して1回でWaitする時間を設定します。\r\n設定値/1000秒間Waitします。\r\n最速値は1です。");
			this.Wait時間NumericUpDown.Value = new decimal(new int[4] { 5, 0, 0, 0 });
			this.Wait間隔Label.AutoSize = true;
			this.Wait間隔Label.Location = new System.Drawing.Point(376, 31);
			this.Wait間隔Label.Name = "Wait間隔Label";
			this.Wait間隔Label.Size = new System.Drawing.Size(51, 12);
			this.Wait間隔Label.TabIndex = 1;
			this.Wait間隔Label.Text = "Wait間隔";
			this.Wait時間Label.AutoSize = true;
			this.Wait時間Label.Location = new System.Drawing.Point(514, 31);
			this.Wait時間Label.Name = "Wait時間Label";
			this.Wait時間Label.Size = new System.Drawing.Size(51, 12);
			this.Wait時間Label.TabIndex = 3;
			this.Wait時間Label.Text = "Wait時間";
			base.AutoScaleDimensions = new System.Drawing.SizeF(6f, 12f);
			base.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
			base.ClientSize = new System.Drawing.Size(634, 187);
			base.Controls.Add(this.Wait時間NumericUpDown);
			base.Controls.Add(this.Wait時間Label);
			base.Controls.Add(this.Wait間隔NumericUpDown);
			base.Controls.Add(this.文字コード選択Label);
			base.Controls.Add(this.Wait間隔Label);
			base.Controls.Add(this.文字コード選択ComboBox);
			base.Controls.Add(this.実行);
			base.Controls.Add(this.経過表示Label);
			base.Controls.Add(this.参照ファイルLabel);
			base.Controls.Add(this.参照ファイル名表示);
			base.Controls.Add(this.処理進行状況);
			base.Controls.Add(this.参照);
			base.Controls.Add(this.出力オプションGroupBox);
			base.MaximizeBox = false;
			this.MaximumSize = new System.Drawing.Size(650, 226);
			this.MinimumSize = new System.Drawing.Size(650, 226);
			base.Name = "PokeTEXT_Form";
			this.Text = "PokeTEXT - Ver.1.0.0.0";
			this.出力オプションGroupBox.ResumeLayout(false);
			this.出力オプションGroupBox.PerformLayout();
			((System.ComponentModel.ISupportInitialize)this.蓄積データ出力NumericUpDown).EndInit();
			((System.ComponentModel.ISupportInitialize)this.Wait間隔NumericUpDown).EndInit();
			((System.ComponentModel.ISupportInitialize)this.Wait時間NumericUpDown).EndInit();
			base.ResumeLayout(false);
			base.PerformLayout();
		}
	}
}
